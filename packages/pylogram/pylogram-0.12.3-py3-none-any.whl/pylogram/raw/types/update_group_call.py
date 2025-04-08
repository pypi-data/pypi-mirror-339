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


class UpdateGroupCall(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pylogram.raw.base.Update`.

    Details:
        - Layer: ``201``
        - ID: ``97D64341``

    Parameters:
        call (:obj:`GroupCall <pylogram.raw.base.GroupCall>`):
            N/A

        chat_id (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["call", "chat_id"]

    ID = 0x97d64341
    QUALNAME = "types.UpdateGroupCall"

    def __init__(self, *, call: "raw.base.GroupCall", chat_id: Optional[int] = None) -> None:
        self.call = call  # GroupCall
        self.chat_id = chat_id  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateGroupCall":
        
        flags = Int.read(b)
        
        chat_id = Long.read(b) if flags & (1 << 0) else None
        call = TLObject.read(b)
        
        return UpdateGroupCall(call=call, chat_id=chat_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.chat_id is not None else 0
        b.write(Int(flags))
        
        if self.chat_id is not None:
            b.write(Long(self.chat_id))
        
        b.write(self.call.write())
        
        return b.getvalue()
