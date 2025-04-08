#  Pylogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2023 Dan <https://github.com/delivrance>
#  Copyright (C) 2023-2024 Pylakey <https://github.com/pylakey>
#
#  This file is part of Pylogram.
#
#  Pylogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pylogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pylogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pylogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pylogram.raw.core import TLObject
from pylogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class UpdatePaidMessagesPrice(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``201``
        - ID: ``FC84653F``

    Parameters:
        channel (:obj:`InputChannel <pylogram.raw.base.InputChannel>`):
            N/A

        send_paid_messages_stars (``int`` ``64-bit``):
            N/A

    Returns:
        :obj:`Updates <pylogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "send_paid_messages_stars"]

    ID = 0xfc84653f
    QUALNAME = "functions.channels.UpdatePaidMessagesPrice"

    def __init__(self, *, channel: "raw.base.InputChannel", send_paid_messages_stars: int) -> None:
        self.channel = channel  # InputChannel
        self.send_paid_messages_stars = send_paid_messages_stars  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePaidMessagesPrice":
        # No flags
        
        channel = TLObject.read(b)
        
        send_paid_messages_stars = Long.read(b)
        
        return UpdatePaidMessagesPrice(channel=channel, send_paid_messages_stars=send_paid_messages_stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Long(self.send_paid_messages_stars))
        
        return b.getvalue()
