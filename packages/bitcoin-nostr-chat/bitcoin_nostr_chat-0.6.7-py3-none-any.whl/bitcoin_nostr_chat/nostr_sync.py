#
# Nostr Sync
# Copyright (C) 2024 Andreas Griffin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import bdkpython as bdk
from bitcoin_qr_tools.data import Data, DataType
from nostr_sdk import Keys, PublicKey, SecretKey
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from bitcoin_nostr_chat import DEFAULT_USE_COMPRESSION
from bitcoin_nostr_chat.bitcoin_dm import BitcoinDM, ChatLabel
from bitcoin_nostr_chat.dialogs import SecretKeyDialog, create_custom_message_box
from bitcoin_nostr_chat.group_chat import GroupChat, NostrProtocol
from bitcoin_nostr_chat.label_connector import LabelConnector
from bitcoin_nostr_chat.protocol_dm import ProtocolDM
from bitcoin_nostr_chat.relay_list import RelayList
from bitcoin_nostr_chat.signals_min import SignalsMin
from bitcoin_nostr_chat.ui.util import chat_color, get_input_text, short_key
from bitcoin_nostr_chat.utils import filtered_for_init

from .chat import Chat
from .group_chat import GroupChat, Keys
from .html import html_f
from .signals_min import SignalsMin
from .ui.ui import UI

logger = logging.getLogger(__name__)


def is_binary(file_path: str):
    """Check if a file is binary or text.

    Returns True if binary, False if text.
    """
    try:
        with open(file_path, "r") as f:
            for chunk in iter(lambda: f.read(1024), ""):
                if "\0" in chunk:  # found null byte
                    return True
    except UnicodeDecodeError:
        return True

    return False


def file_to_str(file_path: str):
    if is_binary(file_path):
        with open(file_path, "rb") as f:
            return bytes(f.read()).hex()
    else:
        with open(file_path, "r") as f:
            return f.read()


class BaseNostrSync(QObject):

    signal_set_alias = pyqtSignal(str, str)
    signal_remove_trusted_device = pyqtSignal(str)
    signal_add_trusted_device = pyqtSignal(str)
    signal_trusted_device_published_trust_me_back = pyqtSignal(str)

    def __init__(
        self,
        network: bdk.Network,
        nostr_protocol: NostrProtocol,
        group_chat: GroupChat,
        signals_min: SignalsMin,
        individual_chats_visible=True,
        hide_data_types_in_chat: tuple[DataType] = (DataType.LabelsBip329,),
        use_compression=DEFAULT_USE_COMPRESSION,
        debug=False,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent=parent)
        self.network = network
        self.debug = debug
        self.nostr_protocol = nostr_protocol
        self.group_chat = group_chat
        self.hide_data_types_in_chat = hide_data_types_in_chat
        self.signals_min = signals_min
        self.use_compression = use_compression

        self.ui = UI(
            my_keys=self.group_chat.dm_connection.async_dm_connection.keys,
            individual_chats_visible=individual_chats_visible,
            signals_min=signals_min,
            get_relay_list=self.group_chat.dm_connection.get_connected_relays,
        )
        self.signal_set_alias.connect(self.ui.device_manager.on_set_alias)

        self.nostr_protocol.signal_dm.connect(self.on_signal_protocol_dm)
        self.group_chat.signal_dm.connect(self.on_dm)

        self.ui.signal_set_relays.connect(self.on_set_relays)
        self.ui.device_manager.untrusted.signal_trust_device.connect(self.on_gui_signal_trust_device)
        self.ui.device_manager.trusted.signal_untrust_device.connect(self.untrust_device)
        self.ui.signal_reset_keys.connect(self.reset_own_key)
        self.ui.signal_set_keys.connect(self.set_own_key)
        self.ui.signal_close_event.connect(self.stop)
        self.ui.device_manager.signal_set_alias.connect(self.signal_set_alias)

    def on_gui_signal_trust_device(self, pub_key_bech32: str):
        self.trust_device(pub_key_bech32=pub_key_bech32)
        # the trusted device maybe has sent messages already
        # and we have received a message, but did not trust the author
        # and therefore dismised the message.
        # Here we resubscribe, to get all the messages again
        self.group_chat.dm_connection.queue_coroutine(
            self.group_chat.dm_connection.async_dm_connection.notification_handler.replay_untrusted_events
        )

    def stop(self):
        self.group_chat.dm_connection.stop()
        self.nostr_protocol.dm_connection.stop()

    def on_set_relays(self, relay_list: RelayList):
        logger.info(f"Setting relay_list {relay_list} ")
        self.group_chat.set_relay_list(relay_list)
        self.nostr_protocol.set_relay_list(relay_list)
        self.publish_my_key_in_protocol(force=True)
        logger.info(f"Done Setting relay_list {relay_list} ")

    def is_me(self, public_key: PublicKey) -> bool:
        return public_key.to_bech32() == self.group_chat.my_public_key().to_bech32()

    def set_own_key(self):
        nsec = SecretKeyDialog().get_secret_key()
        if not nsec:
            return
        try:
            keys = Keys(SecretKey.parse(nsec))
            self.reset_own_key(keys=keys)
        except:
            create_custom_message_box(
                QMessageBox.Icon.Warning, "Error", f"Error in importing the nsec {nsec}"
            )
            return

    def reset_own_key(self, keys: Keys | None = None):
        self.group_chat.renew_own_key(keys=keys)
        self.ui.set_my_keys(self.group_chat.dm_connection.async_dm_connection.keys)
        self.publish_my_key_in_protocol()

        # ask the members to trust my new key again (they need to manually approve)
        for member in self.group_chat.members:
            self.nostr_protocol.publish_trust_me_back(
                author_public_key=self.group_chat.my_public_key(),
                recipient_public_key=member,
            )

    @classmethod
    def from_keys(
        cls,
        network: bdk.Network,
        protocol_keys: Keys,
        device_keys: Keys,
        signals_min: SignalsMin,
        individual_chats_visible=True,
        use_compression=DEFAULT_USE_COMPRESSION,
        parent: QObject | None = None,
    ):
        nostr_protocol = NostrProtocol(
            network=network,
            keys=protocol_keys,
            use_compression=use_compression,
            sync_start=None,
            parent=parent,
        )
        group_chat = GroupChat(
            network=network,
            keys=device_keys,
            use_compression=use_compression,
            sync_start=None,
            parent=parent,
        )
        return cls(
            network=network,
            nostr_protocol=nostr_protocol,
            group_chat=group_chat,
            individual_chats_visible=individual_chats_visible,
            signals_min=signals_min,
            use_compression=use_compression,
            parent=parent,
        )

    def dump(self) -> Dict[str, Any]:
        d = {}
        # exclude my own key. It's pointless to save and
        # later replay (internally) protocol messages that i sent previously
        d["nostr_protocol"] = self.nostr_protocol.dump()
        d["group_chat"] = self.group_chat.dump()
        d["individual_chats_visible"] = self.ui.individual_chats_visible
        d["network"] = self.network.name
        d["debug"] = self.debug
        return d

    @classmethod
    def from_dump(
        cls,
        d: Dict[str, Any],
        signals_min: SignalsMin,
        parent: QObject | None = None,
    ):
        d["nostr_protocol"] = NostrProtocol.from_dump(d["nostr_protocol"])
        d["group_chat"] = GroupChat.from_dump(d["group_chat"])
        d["network"] = bdk.Network[d["network"]]

        sync = cls(**filtered_for_init(d, BaseNostrSync), signals_min=signals_min, parent=parent)

        # add the gui elements for the trusted members
        for member in sync.group_chat.members:
            if sync.is_me(member):
                # do not add myself as a device
                continue
            pub_key_bech32 = member.to_bech32()
            sync.ui.device_manager.create_trusted_device(
                pub_key_bech32=pub_key_bech32, alias=sync.group_chat.aliases.get(pub_key_bech32)
            )

        # restore/replay chat texts
        sync.nostr_protocol.dm_connection.replay_events_from_dump()
        sync.group_chat.dm_connection.replay_events_from_dump()
        return sync

    def subscribe(self):
        self.nostr_protocol.subscribe()
        self.group_chat.subscribe()
        self.publish_my_key_in_protocol()

    def unsubscribe(self):
        self.nostr_protocol.dm_connection.unsubscribe_all()
        self.group_chat.dm_connection.unsubscribe_all()

    def publish_my_key_in_protocol(self, force=False):
        self.nostr_protocol.publish_public_key(self.group_chat.my_public_key(), force=force)

    def on_dm(self, dm: BitcoinDM):
        if not dm.author:
            logger.debug(f"Dropping {dm}, because not author, and with that author can be determined.")
            return

        elif dm.label == ChatLabel.DistrustMeRequest and not self.is_me(dm.author):
            self.untrust_key(dm.author)
        elif dm.label == ChatLabel.DeleteMeRequest and not self.is_me(dm.author):
            self.untrust_key(dm.author)
            self.ui.device_manager.remove_from_all(dm.author.to_bech32())

    def untrust_key(self, member: PublicKey):
        self.ui.device_manager.untrust(member.to_bech32())
        self.group_chat.remove_member(member)

    def get_singlechat_counterparty(self, dm: BitcoinDM) -> Optional[str]:
        if dm.label != ChatLabel.SingleRecipient:
            return None

        if not dm.author:
            return None

        # if I sent it, and there is a intended_recipient
        # then the dm is a message from me to intended_recipient,
        # and should be displayed in trusted_device of the  intended_recipient
        if self.is_me(dm.author):
            if dm.intended_recipient:
                return dm.intended_recipient
            return None
        else:
            return dm.author.to_bech32()

    def file_to_dm(self, file_content: str, label: ChatLabel, file_name: str) -> BitcoinDM:
        bitcoin_data = Data.from_str(file_content, network=self.network)
        if not bitcoin_data:
            raise Exception(
                self.tr("Could not recognize {file_content} as BitcoinData").format(file_content=file_content)
            )
        dm = BitcoinDM(
            label=label,
            description=file_name,
            event=None,
            data=bitcoin_data,
            use_compression=self.use_compression,
            created_at=datetime.now(),
        )
        return dm

    def on_signal_protocol_dm(self, dm: ProtocolDM):
        if self.is_me(PublicKey.parse(dm.public_key_bech32)):
            # if I'm the autor do noting
            return
        if self.ui.device_manager.trusted.get_device(dm.public_key_bech32):
            self.signal_trusted_device_published_trust_me_back.emit(dm.public_key_bech32)
            return

        self.ui.device_manager.create_untrusted_device(
            pub_key_bech32=dm.public_key_bech32,
        )

        if dm.please_trust_public_key_bech32 and datetime.now() - dm.created_at < timedelta(hours=2):
            # the message is a request to trust the author
            untrusted_device = self.ui.device_manager.untrusted.get_device(dm.public_key_bech32)
            if not untrusted_device:
                logger.warning(f"For {dm.public_key_bech32} could not be found an untrusted device")
                return
            untrusted_device.set_button_status_to_accept()

    def untrust_device(self, pub_key_bech32: str):
        self.group_chat.remove_member(PublicKey.parse(pub_key_bech32))
        self.ui.device_manager.untrust(pub_key_bech32=pub_key_bech32)

        self.signal_remove_trusted_device.emit(pub_key_bech32)

        if pub_key_bech32 in self.group_chat.aliases:
            del self.group_chat.aliases[pub_key_bech32]

    def trust_device(self, pub_key_bech32: str, show_message=True):
        device_public_key = PublicKey.parse(pub_key_bech32)
        self.group_chat.add_member(device_public_key)

        untrusted_device = self.ui.device_manager.untrusted.get_device(pub_key_bech32)
        self.ui.device_manager.untrusted.remove(pub_key_bech32=pub_key_bech32)
        self.ui.device_manager.create_trusted_device(pub_key_bech32=pub_key_bech32)

        if show_message and untrusted_device and not untrusted_device.trust_request_active():
            QMessageBox.information(
                self.ui,
                self.tr("Go to {untrusted}").format(untrusted=short_key(untrusted_device.pub_key_bech32)),
                self.tr(
                    "To complete the connection, accept my {id} request on the other device {other}."
                ).format(
                    id=html_f(
                        short_key(self.group_chat.my_public_key().to_bech32()),
                        bf=True,
                    ),
                    other=html_f(short_key(untrusted_device.pub_key_bech32), bf=True),
                ),
            )

        self.signal_add_trusted_device.emit(pub_key_bech32)

        self.nostr_protocol.publish_trust_me_back(
            author_public_key=self.group_chat.my_public_key(),
            recipient_public_key=device_public_key,
        )

        alias = get_input_text(
            placeholder_text=self.tr("Enter a name of device with {npub}").format(npub=pub_key_bech32),
            title="Device name",
            textcolor=chat_color(pub_key_bech32),
        )
        if alias:
            self.signal_set_alias.emit(pub_key_bech32, alias)


class NostrSync(BaseNostrSync):
    def __init__(
        self,
        network: bdk.Network,
        nostr_protocol: NostrProtocol,
        group_chat: GroupChat,
        signals_min: SignalsMin,
        individual_chats_visible=True,
        hide_data_types_in_chat: tuple[DataType] = (DataType.LabelsBip329,),
        use_compression=DEFAULT_USE_COMPRESSION,
        debug=False,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(
            network,
            nostr_protocol,
            group_chat,
            signals_min,
            individual_chats_visible,
            hide_data_types_in_chat,
            use_compression,
            debug,
            parent,
        )

        self.label_connector = LabelConnector(
            group_chat=self.group_chat, signals_min=signals_min, debug=debug
        )

        self.chat = Chat(
            network=network,
            group_chat=self.group_chat,
            signals_min=signals_min,
            use_compression=use_compression,
            display_labels=[ChatLabel.GroupChat, ChatLabel.SingleRecipient],
            send_label=ChatLabel.GroupChat,
        )
        self.ui.tabs.addTab(self.chat.gui, self.tr("Group Chat"))
        self.signal_set_alias.connect(self.chat.on_set_alias)


class NostrSyncWithSingleChats(BaseNostrSync):

    def __init__(
        self,
        network: bdk.Network,
        nostr_protocol: NostrProtocol,
        group_chat: GroupChat,
        signals_min: SignalsMin,
        individual_chats_visible=True,
        hide_data_types_in_chat: tuple[DataType] = (DataType.LabelsBip329,),
        use_compression=DEFAULT_USE_COMPRESSION,
        debug=False,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(
            network,
            nostr_protocol,
            group_chat,
            signals_min,
            individual_chats_visible,
            hide_data_types_in_chat,
            use_compression,
            debug,
            parent,
        )

        self.label_connector = LabelConnector(
            group_chat=self.group_chat, signals_min=signals_min, debug=debug
        )

        self.chat = Chat(
            network=network,
            group_chat=self.group_chat,
            signals_min=signals_min,
            use_compression=use_compression,
            display_labels=[ChatLabel.GroupChat],
            send_label=ChatLabel.GroupChat,
        )
        self.ui.tabs.addTab(self.chat.gui, self.tr("Chat"))

        self.chats: Dict[str, Chat] = {}

        self.signal_add_trusted_device.connect(self.add_chat_for_trusted_device)
        self.signal_remove_trusted_device.connect(self.remove_chat_for_trusted_device)
        self.signal_set_alias.connect(self.chat.on_set_alias)

    def add_chat_for_trusted_device(self, pub_key_bech32: str):
        chat = Chat(
            network=self.network,
            group_chat=self.group_chat,
            signals_min=self.signals_min,
            use_compression=self.use_compression,
            restrict_to_counterparties=[PublicKey.parse(pub_key_bech32)],
            display_labels=[ChatLabel.SingleRecipient],
            send_label=ChatLabel.SingleRecipient,
        )
        self.chats[pub_key_bech32] = chat
        self.ui.tabs.addTab(chat.gui, short_key(pub_key_bech32))

    def remove_chat_for_trusted_device(self, pub_key_bech32: str):
        if pub_key_bech32 not in self.chats:
            return
        chat = self.chats[pub_key_bech32]

        index = self.ui.tabs.indexOf(chat.gui)
        if index >= 0:
            self.ui.tabs.removeTab(index)

        del self.chats[pub_key_bech32]
