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


class PreviewInfo(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pylogram.raw.base.bots.PreviewInfo`.

    Details:
        - Layer: ``201``
        - ID: ``CA71D64``

    Parameters:
        media (List of :obj:`BotPreviewMedia <pylogram.raw.base.BotPreviewMedia>`):
            N/A

        lang_codes (List of ``str``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pylogram.raw.functions

        .. autosummary::
            :nosignatures:

            bots.GetPreviewInfo
    """

    __slots__: List[str] = ["media", "lang_codes"]

    ID = 0xca71d64
    QUALNAME = "types.bots.PreviewInfo"

    def __init__(self, *, media: List["raw.base.BotPreviewMedia"], lang_codes: List[str]) -> None:
        self.media = media  # Vector<BotPreviewMedia>
        self.lang_codes = lang_codes  # Vector<string>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PreviewInfo":
        # No flags
        
        media = TLObject.read(b)
        
        lang_codes = TLObject.read(b, String)
        
        return PreviewInfo(media=media, lang_codes=lang_codes)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.media))
        
        b.write(Vector(self.lang_codes, String))
        
        return b.getvalue()
