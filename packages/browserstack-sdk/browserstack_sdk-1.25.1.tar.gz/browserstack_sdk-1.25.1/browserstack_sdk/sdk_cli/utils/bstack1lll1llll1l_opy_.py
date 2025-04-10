# coding: UTF-8
import sys
bstack11l1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1ll1l1_opy_ (bstack1l1ll1_opy_):
    global bstack1l111ll_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1ll1_opy_ [-1])
    bstack111llll_opy_ = bstack1l1ll1_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1lll1ll_opy_ % len (bstack111llll_opy_)
    bstack1l1l1l_opy_ = bstack111llll_opy_ [:bstack1l1l11l_opy_] + bstack111llll_opy_ [bstack1l1l11l_opy_:]
    if bstack11l1ll1_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack11ll111_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack1l1ll1111l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lllll11111_opy_:
    bstack1ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡻࡴࡪ࡮࡬ࡸࡾࠦ࡭ࡦࡶ࡫ࡳࡩࡹࠠࡵࡱࠣࡷࡪࡺࠠࡢࡰࡧࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࠣࡱࡪࡺࡡࡥࡣࡷࡥ࠳ࠐࠠࠡࠢࠣࡍࡹࠦ࡭ࡢ࡫ࡱࡸࡦ࡯࡮ࡴࠢࡷࡻࡴࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡳࡪࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࡇࡤࡧ࡭ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡧࡱࡸࡷࡿࠠࡪࡵࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡤࡨࠤࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡤࠡࡣࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢ࠻ࠢࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡻࡧ࡬ࡶࡧࡶࠦ࠿࡛ࠦ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡤ࡫ࠥࡼࡡ࡭ࡷࡨࡷࡢࠐࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠨࠢࠣᔜ")
    _1l1111ll111_opy_: Dict[str, Dict[str, Any]] = {}
    _1l1111l1lll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1ll111l11l_opy_: str, key_value: str, bstack1l1111l1l1l_opy_: bool = False) -> None:
        if not bstack1ll111l11l_opy_ or not key_value or bstack1ll111l11l_opy_.strip() == bstack1ll1l1_opy_ (u"ࠣࠤᔝ") or key_value.strip() == bstack1ll1l1_opy_ (u"ࠤࠥᔞ"):
            logger.error(bstack1ll1l1_opy_ (u"ࠥ࡯ࡪࡿ࡟࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢ࡮ࡩࡾࡥࡶࡢ࡮ࡸࡩࠥࡳࡵࡴࡶࠣࡦࡪࠦ࡮ࡰࡰ࠰ࡲࡺࡲ࡬ࠡࡣࡱࡨࠥࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠣᔟ"))
        values: List[str] = bstack1lllll11111_opy_.bstack1l1111l1ll1_opy_(key_value)
        bstack1l1111l11l1_opy_ = {bstack1ll1l1_opy_ (u"ࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣᔠ"): bstack1ll1l1_opy_ (u"ࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨᔡ"), bstack1ll1l1_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᔢ"): values}
        bstack1l1111l1l11_opy_ = bstack1lllll11111_opy_._1l1111l1lll_opy_ if bstack1l1111l1l1l_opy_ else bstack1lllll11111_opy_._1l1111ll111_opy_
        if bstack1ll111l11l_opy_ in bstack1l1111l1l11_opy_:
            bstack1l1111l1111_opy_ = bstack1l1111l1l11_opy_[bstack1ll111l11l_opy_]
            bstack1l1111ll11l_opy_ = bstack1l1111l1111_opy_.get(bstack1ll1l1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᔣ"), [])
            for val in values:
                if val not in bstack1l1111ll11l_opy_:
                    bstack1l1111ll11l_opy_.append(val)
            bstack1l1111l1111_opy_[bstack1ll1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᔤ")] = bstack1l1111ll11l_opy_
        else:
            bstack1l1111l1l11_opy_[bstack1ll111l11l_opy_] = bstack1l1111l11l1_opy_
    @staticmethod
    def bstack1l11llll111_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lllll11111_opy_._1l1111ll111_opy_
    @staticmethod
    def bstack1l1111l111l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lllll11111_opy_._1l1111l1lll_opy_
    @staticmethod
    def bstack1l1111l1ll1_opy_(bstack1l1111l11ll_opy_: str) -> List[str]:
        bstack1ll1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡱ࡮࡬ࡸࡸࠦࡴࡩࡧࠣ࡭ࡳࡶࡵࡵࠢࡶࡸࡷ࡯࡮ࡨࠢࡥࡽࠥࡩ࡯࡮࡯ࡤࡷࠥࡽࡨࡪ࡮ࡨࠤࡷ࡫ࡳࡱࡧࡦࡸ࡮ࡴࡧࠡࡦࡲࡹࡧࡲࡥ࠮ࡳࡸࡳࡹ࡫ࡤࠡࡵࡸࡦࡸࡺࡲࡪࡰࡪࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡪࡾࡡ࡮ࡲ࡯ࡩ࠿ࠦࠧࡢ࠮ࠣࠦࡧ࠲ࡣࠣ࠮ࠣࡨࠬࠦ࠭࠿ࠢ࡞ࠫࡦ࠭ࠬࠡࠩࡥ࠰ࡨ࠭ࠬࠡࠩࡧࠫࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᔥ")
        pattern = re.compile(bstack1ll1l1_opy_ (u"ࡵࠫࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨࡼࠩ࡝ࡡ࠰ࡢ࠱ࠩࠨᔦ"))
        result = []
        for match in pattern.finditer(bstack1l1111l11ll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1ll1l1_opy_ (u"࡚ࠦࡺࡩ࡭࡫ࡷࡽࠥࡩ࡬ࡢࡵࡶࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤ࡮ࡴࡳࡵࡣࡱࡸ࡮ࡧࡴࡦࡦࠥᔧ"))