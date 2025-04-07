# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack111_opy_ = 7
def bstack11l1l11_opy_ (bstack11lll_opy_):
    global bstack1l11l11_opy_
    bstack1l1l1_opy_ = ord (bstack11lll_opy_ [-1])
    bstack1l111ll_opy_ = bstack11lll_opy_ [:-1]
    bstack11l_opy_ = bstack1l1l1_opy_ % len (bstack1l111ll_opy_)
    bstack11l111l_opy_ = bstack1l111ll_opy_ [:bstack11l_opy_] + bstack1l111ll_opy_ [bstack11l_opy_:]
    if bstack11111ll_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack1l_opy_)
import os
import re
from enum import Enum
bstack111111l11_opy_ = {
  bstack11l1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᗙ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࠬᗚ"),
  bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᗛ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ࠭ᗜ"),
  bstack11l1l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᗝ"): bstack11l1l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᗞ"),
  bstack11l1l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᗟ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧᗠ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᗡ"): bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࠪᗢ"),
  bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᗣ"): bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪᗤ"),
  bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᗥ"): bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᗦ"),
  bstack11l1l11_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᗧ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠭ᗨ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧᗩ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳࡹ࡯࡭ࡧࠪᗪ"),
  bstack11l1l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᗫ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᗬ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪᗭ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪᗮ"),
  bstack11l1l11_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧᗯ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡸ࡬ࡨࡪࡵࠧᗰ"),
  bstack11l1l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩᗱ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩᗲ"),
  bstack11l1l11_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᗳ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᗴ"),
  bstack11l1l11_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᗵ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᗶ"),
  bstack11l1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᗷ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᗸ"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗹ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᗺ"),
  bstack11l1l11_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬᗻ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬᗼ"),
  bstack11l1l11_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᗽ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᗾ"),
  bstack11l1l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᗿ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᘀ"),
  bstack11l1l11_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧᘁ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧᘂ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᘃ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᘄ"),
  bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨᘅ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨᘆ"),
  bstack11l1l11_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬᘇ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬᘈ"),
  bstack11l1l11_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧᘉ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧᘊ"),
  bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫᘋ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫᘌ"),
  bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᘍ"): bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᘎ"),
  bstack11l1l11_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩᘏ"): bstack11l1l11_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫᘐ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᘑ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᘒ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩᘓ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩᘔ"),
  bstack11l1l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬᘕ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬᘖ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᘗ"): bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨᘘ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᘙ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᘚ"),
  bstack11l1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᘛ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡴࡻࡲࡤࡧࠪᘜ"),
  bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᘝ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᘞ"),
  bstack11l1l11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩᘟ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡓࡧ࡭ࡦࠩᘠ"),
  bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬᘡ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬᘢ"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨᘣ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨᘤ"),
  bstack11l1l11_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫᘥ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫᘦ"),
  bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᘧ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᘨ"),
  bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᘩ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᘪ")
}
bstack11llll11l11_opy_ = [
  bstack11l1l11_opy_ (u"ࠬࡵࡳࠨᘫ"),
  bstack11l1l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᘬ"),
  bstack11l1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᘭ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᘮ"),
  bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᘯ"),
  bstack11l1l11_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᘰ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᘱ"),
]
bstack111lll1ll_opy_ = {
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᘲ"): [bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᘳ"), bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡓࡇࡍࡆࠩᘴ")],
  bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᘵ"): bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬᘶ"),
  bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᘷ"): bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧᘸ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᘹ"): bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠫᘺ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᘻ"): bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᘼ"),
  bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᘽ"): bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡗࡤࡖࡅࡓࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫᘾ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᘿ"): bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪᙀ"),
  bstack11l1l11_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᙁ"): bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫᙂ"),
  bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࠬᙃ"): [bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࡤࡏࡄࠨᙄ"), bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕ࠭ᙅ")],
  bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᙆ"): bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡎࡒࡋࡑࡋࡖࡆࡎࠪᙇ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᙈ"): bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᙉ"),
  bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᙊ"): bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞࠭ᙋ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᙌ"): bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘ࡚ࡘࡂࡐࡕࡆࡅࡑࡋࠧᙍ")
}
bstack1ll1llllll_opy_ = {
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᙎ"): [bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡢࡲࡦࡳࡥࠨᙏ"), bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡒࡦࡳࡥࠨᙐ")],
  bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᙑ"): [bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡠ࡭ࡨࡽࠬᙒ"), bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᙓ")],
  bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᙔ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᙕ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᙖ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᙗ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᙘ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᙙ"),
  bstack11l1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᙚ"): [bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡵࡶࠧᙛ"), bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᙜ")],
  bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᙝ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᙞ"),
  bstack11l1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᙟ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᙠ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧᙡ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࠧᙢ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᙣ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᙤ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᙥ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᙦ")
}
bstack1l11l1l1l_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙧ"): bstack11l1l11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᙨ"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙩ"): [bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᙪ"), bstack11l1l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᙫ")],
  bstack11l1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᙬ"): bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭᙭"),
  bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭᙮"): bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᙯ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᙰ"): [bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᙱ"), bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᙲ")],
  bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙳ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᙴ"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ᙵ"): bstack11l1l11_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨᙶ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᙷ"): [bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᙸ"), bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᙹ")],
  bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᙺ"): [bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࡴࠩᙻ"), bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࠩᙼ")]
}
bstack111l11lll_opy_ = [
  bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᙽ"),
  bstack11l1l11_opy_ (u"ࠫࡵࡧࡧࡦࡎࡲࡥࡩ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧᙾ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫᙿ"),
  bstack11l1l11_opy_ (u"࠭ࡳࡦࡶ࡚࡭ࡳࡪ࡯ࡸࡔࡨࡧࡹ࠭ "),
  bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡴࡻࡴࡴࠩᚁ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡷࡶ࡮ࡩࡴࡇ࡫࡯ࡩࡎࡴࡴࡦࡴࡤࡧࡹࡧࡢࡪ࡮࡬ࡸࡾ࠭ᚂ"),
  bstack11l1l11_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬᚃ"),
  bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚄ"),
  bstack11l1l11_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚅ"),
  bstack11l1l11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚆ"),
  bstack11l1l11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᚇ"),
  bstack11l1l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᚈ"),
]
bstack1l1lll11ll_opy_ = [
  bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᚉ"),
  bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚊ"),
  bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚋ"),
  bstack11l1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᚌ"),
  bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᚍ"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᚎ"),
  bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᚏ"),
  bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᚐ"),
  bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᚑ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨᚒ"),
  bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᚓ"),
  bstack11l1l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᚔ"),
  bstack11l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡚ࡡࡨࠩᚕ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᚖ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᚗ"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᚘ"),
  bstack11l1l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠲ࠩᚙ"),
  bstack11l1l11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠴ࠪᚚ"),
  bstack11l1l11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠶ࠫ᚛"),
  bstack11l1l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠸ࠬ᚜"),
  bstack11l1l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠺࠭᚝"),
  bstack11l1l11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠼ࠧ᚞"),
  bstack11l1l11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠷ࠨ᚟"),
  bstack11l1l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠹ࠩᚠ"),
  bstack11l1l11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠻ࠪᚡ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᚢ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᚣ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᚤ"),
  bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᚥ"),
  bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᚦ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚧ")
]
bstack11llll111l1_opy_ = [
  bstack11l1l11_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᚨ"),
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᚩ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᚪ"),
  bstack11l1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᚫ"),
  bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡖࡲࡪࡱࡵ࡭ࡹࡿࠧᚬ"),
  bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᚭ"),
  bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡤ࡫ࠬᚮ"),
  bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᚯ"),
  bstack11l1l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᚰ"),
  bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᚱ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚲ"),
  bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᚳ"),
  bstack11l1l11_opy_ (u"ࠩࡲࡷࠬᚴ"),
  bstack11l1l11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚵ"),
  bstack11l1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪᚶ"),
  bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᚷ"),
  bstack11l1l11_opy_ (u"࠭ࡲࡦࡩ࡬ࡳࡳ࠭ᚸ"),
  bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᚹ"),
  bstack11l1l11_opy_ (u"ࠨ࡯ࡤࡧ࡭࡯࡮ࡦࠩᚺ"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭ᚻ"),
  bstack11l1l11_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨᚼ"),
  bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᚽ"),
  bstack11l1l11_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫᚾ"),
  bstack11l1l11_opy_ (u"࠭࡮ࡰࡒࡤ࡫ࡪࡒ࡯ࡢࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᚿ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨᛀ"),
  bstack11l1l11_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᛁ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᛂ"),
  bstack11l1l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡩࡳࡪࡋࡦࡻࡶࠫᛃ"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᛄ"),
  bstack11l1l11_opy_ (u"ࠬࡴ࡯ࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠩᛅ"),
  bstack11l1l11_opy_ (u"࠭ࡣࡩࡧࡦ࡯࡚ࡘࡌࠨᛆ"),
  bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᛇ"),
  bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡄࡱࡲ࡯࡮࡫ࡳࠨᛈ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡥࡵࡺࡵࡳࡧࡆࡶࡦࡹࡨࠨᛉ"),
  bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᛊ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᛋ"),
  bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡘࡨࡶࡸ࡯࡯࡯ࠩᛌ"),
  bstack11l1l11_opy_ (u"࠭࡮ࡰࡄ࡯ࡥࡳࡱࡐࡰ࡮࡯࡭ࡳ࡭ࠧᛍ"),
  bstack11l1l11_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ᛎ"),
  bstack11l1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡍࡱࡪࡷࠬᛏ"),
  bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡋࡧࠫᛐ"),
  bstack11l1l11_opy_ (u"ࠪࡨࡪࡪࡩࡤࡣࡷࡩࡩࡊࡥࡷ࡫ࡦࡩࠬᛑ"),
  bstack11l1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡔࡦࡸࡡ࡮ࡵࠪᛒ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡨࡰࡰࡨࡒࡺࡳࡢࡦࡴࠪᛓ"),
  bstack11l1l11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫᛔ"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡔࡶࡴࡪࡱࡱࡷࠬᛕ"),
  bstack11l1l11_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭ᛖ"),
  bstack11l1l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᛗ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᛘ"),
  bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡆ࡮ࡵ࡭ࡦࡶࡵ࡭ࡨ࠭ᛙ"),
  bstack11l1l11_opy_ (u"ࠬࡼࡩࡥࡧࡲ࡚࠷࠭ᛚ"),
  bstack11l1l11_opy_ (u"࠭࡭ࡪࡦࡖࡩࡸࡹࡩࡰࡰࡌࡲࡸࡺࡡ࡭࡮ࡄࡴࡵࡹࠧᛛ"),
  bstack11l1l11_opy_ (u"ࠧࡦࡵࡳࡶࡪࡹࡳࡰࡕࡨࡶࡻ࡫ࡲࠨᛜ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᛝ"),
  bstack11l1l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡇࡩࡶࠧᛞ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᛟ"),
  bstack11l1l11_opy_ (u"ࠫࡸࡿ࡮ࡤࡖ࡬ࡱࡪ࡝ࡩࡵࡪࡑࡘࡕ࠭ᛠ"),
  bstack11l1l11_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᛡ"),
  bstack11l1l11_opy_ (u"࠭ࡧࡱࡵࡏࡳࡨࡧࡴࡪࡱࡱࠫᛢ"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨᛣ"),
  bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨᛤ"),
  bstack11l1l11_opy_ (u"ࠩࡩࡳࡷࡩࡥࡄࡪࡤࡲ࡬࡫ࡊࡢࡴࠪᛥ"),
  bstack11l1l11_opy_ (u"ࠪࡼࡲࡹࡊࡢࡴࠪᛦ"),
  bstack11l1l11_opy_ (u"ࠫࡽࡳࡸࡋࡣࡵࠫᛧ"),
  bstack11l1l11_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫᛨ"),
  bstack11l1l11_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᛩ"),
  bstack11l1l11_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨᛪ"),
  bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ᛫"),
  bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᛬"),
  bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ᛭"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡪࡩࡱࡅࡵࡶࠧᛮ"),
  bstack11l1l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࡴࠩᛯ"),
  bstack11l1l11_opy_ (u"࠭ࡣࡢࡰࡤࡶࡾ࠭ᛰ"),
  bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᛱ"),
  bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᛲ"),
  bstack11l1l11_opy_ (u"ࠩ࡬ࡩࠬᛳ"),
  bstack11l1l11_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᛴ"),
  bstack11l1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᛵ"),
  bstack11l1l11_opy_ (u"ࠬࡷࡵࡦࡷࡨࠫᛶ"),
  bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨᛷ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡗࡹࡵࡲࡦࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠨᛸ"),
  bstack11l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡄࡣࡰࡩࡷࡧࡉ࡮ࡣࡪࡩࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧ᛹"),
  bstack11l1l11_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡅࡹࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬ᛺"),
  bstack11l1l11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡊࡰࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭᛻"),
  bstack11l1l11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ᛼"),
  bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡧࡵࡺࡪࡊࡥࡷ࡫ࡦࡩࠬ᛽"),
  bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭᛾"),
  bstack11l1l11_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ᛿"),
  bstack11l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡣࡶࡷࡨࡵࡤࡦࠩᜀ"),
  bstack11l1l11_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡋࡲࡷࡉ࡫ࡶࡪࡥࡨࡗࡪࡺࡴࡪࡰࡪࡷࠬᜁ"),
  bstack11l1l11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡹࡩ࡯࡯ࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪᜂ"),
  bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡵࡶ࡬ࡦࡒࡤࡽࠬᜃ"),
  bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᜄ"),
  bstack11l1l11_opy_ (u"࠭ࡷࡥ࡫ࡲࡗࡪࡸࡶࡪࡥࡨࠫᜅ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᜆ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵࡅࡵࡳࡸࡹࡓࡪࡶࡨࡘࡷࡧࡣ࡬࡫ࡱ࡫ࠬᜇ"),
  bstack11l1l11_opy_ (u"ࠩ࡫࡭࡬࡮ࡃࡰࡰࡷࡶࡦࡹࡴࠨᜈ"),
  bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧᜉ"),
  bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧᜊ"),
  bstack11l1l11_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜋ"),
  bstack11l1l11_opy_ (u"࠭ࡲࡦ࡯ࡲࡺࡪࡏࡏࡔࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࡒ࡯ࡤࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᜌ"),
  bstack11l1l11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩᜍ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᜎ"),
  bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᜏ"),
  bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᜐ"),
  bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜑ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨᜒ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬᜓ"),
  bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡴࡻࡴࡴ᜔ࠩ"),
  bstack11l1l11_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵ᜕ࠫ")
]
bstack1lllll11l_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡹࠫ᜖"): bstack11l1l11_opy_ (u"ࠪࡺࠬ᜗"),
  bstack11l1l11_opy_ (u"ࠫ࡫࠭᜘"): bstack11l1l11_opy_ (u"ࠬ࡬ࠧ᜙"),
  bstack11l1l11_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬ᜚"): bstack11l1l11_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭᜛"),
  bstack11l1l11_opy_ (u"ࠨࡱࡱࡰࡾࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᜜"): bstack11l1l11_opy_ (u"ࠩࡲࡲࡱࡿࡁࡶࡶࡲࡱࡦࡺࡥࠨ᜝"),
  bstack11l1l11_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧ᜞"): bstack11l1l11_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨᜟ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨᜠ"): bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᜡ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪᜢ"): bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᜣ"),
  bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᜤ"): bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᜥ"),
  bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᜦ"): bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨᜧ"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧᜨ"): bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡌࡴࡹࡴࠨᜩ"),
  bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩᜪ"): bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᜫ"),
  bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᜬ"): bstack11l1l11_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᜭ"),
  bstack11l1l11_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᜮ"): bstack11l1l11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᜯ"),
  bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᜰ"): bstack11l1l11_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᜱ"),
  bstack11l1l11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᜲ"): bstack11l1l11_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᜳ"),
  bstack11l1l11_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨ᜴"): bstack11l1l11_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩ᜵"),
  bstack11l1l11_opy_ (u"࠭ࡰࡢࡥࡩ࡭ࡱ࡫ࠧ᜶"): bstack11l1l11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ᜷"),
  bstack11l1l11_opy_ (u"ࠨࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ᜸"): bstack11l1l11_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ᜹"),
  bstack11l1l11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭᜺"): bstack11l1l11_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧ᜻"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭᜼"): bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧ᜽"),
  bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᜾"): bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᜿"),
  bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫᝀ"): bstack11l1l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࠫᝁ")
}
bstack1l111111111_opy_ = bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡩࡵࡪࡸࡦ࠳ࡩ࡯࡮࠱ࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭࠴ࡸࡥ࡭ࡧࡤࡷࡪࡹ࠯࡭ࡣࡷࡩࡸࡺ࠯ࡥࡱࡺࡲࡱࡵࡡࡥࠤᝂ")
bstack11llll1111l_opy_ = bstack11l1l11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠴࡮ࡥࡢ࡮ࡷ࡬ࡨ࡮ࡥࡤ࡭ࠥᝃ")
bstack1lll111ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡦࡦࡶ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡴࡧࡱࡨࡤࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤᝄ")
bstack11ll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡹࡧ࠳࡭ࡻࡢࠨᝅ")
bstack11ll1ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠫᝆ")
bstack1ll111ll1_opy_ = bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸ࠭ᝇ")
bstack11lllll1l11_opy_ = {
  bstack11l1l11_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬᝈ"): 50,
  bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᝉ"): 40,
  bstack11l1l11_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᝊ"): 30,
  bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᝋ"): 20,
  bstack11l1l11_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᝌ"): 10
}
bstack11lll1l1l_opy_ = bstack11lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᝍ")]
bstack11l1ll1111_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᝎ")
bstack111l11ll1_opy_ = bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᝏ")
bstack11ll1l11l_opy_ = bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪᝐ")
bstack1111111ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᝑ")
bstack1ll11lllll_opy_ = bstack11l1l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫᝒ")
bstack11llll11111_opy_ = [bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨᝓ"), bstack11l1l11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ᝔")]
bstack11lll1ll1ll_opy_ = [bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ᝕"), bstack11l1l11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ᝖")]
bstack1ll1l111_opy_ = re.compile(bstack11l1l11_opy_ (u"ࠫࡣࡡ࡜࡝ࡹ࠰ࡡ࠰ࡀ࠮ࠫࠦࠪ᝗"))
bstack11ll11l1_opy_ = [
  bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡐࡤࡱࡪ࠭᝘"),
  bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᝙"),
  bstack11l1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ᝚"),
  bstack11l1l11_opy_ (u"ࠨࡰࡨࡻࡈࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࠬ᝛"),
  bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࠭᝜"),
  bstack11l1l11_opy_ (u"ࠪࡹࡩ࡯ࡤࠨ᝝"),
  bstack11l1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭᝞"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࠬ᝟"),
  bstack11l1l11_opy_ (u"࠭࡯ࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᝠ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻࠬᝡ"),
  bstack11l1l11_opy_ (u"ࠨࡰࡲࡖࡪࡹࡥࡵࠩᝢ"), bstack11l1l11_opy_ (u"ࠩࡩࡹࡱࡲࡒࡦࡵࡨࡸࠬᝣ"),
  bstack11l1l11_opy_ (u"ࠪࡧࡱ࡫ࡡࡳࡕࡼࡷࡹ࡫࡭ࡇ࡫࡯ࡩࡸ࠭ᝤ"),
  bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡗ࡭ࡲ࡯࡮ࡨࡵࠪᝥ"),
  bstack11l1l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕ࡫ࡲࡧࡱࡵࡱࡦࡴࡣࡦࡎࡲ࡫࡬࡯࡮ࡨࠩᝦ"),
  bstack11l1l11_opy_ (u"࠭࡯ࡵࡪࡨࡶࡆࡶࡰࡴࠩᝧ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡴ࡬ࡲࡹࡖࡡࡨࡧࡖࡳࡺࡸࡣࡦࡑࡱࡊ࡮ࡴࡤࡇࡣ࡬ࡰࡺࡸࡥࠨᝨ"),
  bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡆࡩࡴࡪࡸ࡬ࡸࡾ࠭ᝩ"), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡖࡡࡤ࡭ࡤ࡫ࡪ࠭ᝪ"), bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡅࡨࡺࡩࡷ࡫ࡷࡽࠬᝫ"), bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡕࡧࡣ࡬ࡣࡪࡩࠬᝬ"), bstack11l1l11_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡊࡵࡳࡣࡷ࡭ࡴࡴࠧ᝭"),
  bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᝮ"),
  bstack11l1l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚ࡥࡴࡶࡓࡥࡨࡱࡡࡨࡧࡶࠫᝯ"),
  bstack11l1l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࠪᝰ"), bstack11l1l11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡆࡳࡻ࡫ࡲࡢࡩࡨࡉࡳࡪࡉ࡯ࡶࡨࡲࡹ࠭᝱"),
  bstack11l1l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᝲ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡪࡢࡑࡱࡵࡸࠬᝳ"),
  bstack11l1l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡘࡵࡣ࡬ࡧࡷࠫ᝴"),
  bstack11l1l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡔࡪ࡯ࡨࡳࡺࡺࠧ᝵"),
  bstack11l1l11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡷ࡬ࠬ᝶"),
  bstack11l1l11_opy_ (u"ࠨࡣࡹࡨࠬ᝷"), bstack11l1l11_opy_ (u"ࠩࡤࡺࡩࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ᝸"), bstack11l1l11_opy_ (u"ࠪࡥࡻࡪࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ᝹"), bstack11l1l11_opy_ (u"ࠫࡦࡼࡤࡂࡴࡪࡷࠬ᝺"),
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡍࡨࡽࡸࡺ࡯ࡳࡧࠪ᝻"), bstack11l1l11_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡷ࡬ࠬ᝼"), bstack11l1l11_opy_ (u"ࠧ࡬ࡧࡼࡷࡹࡵࡲࡦࡒࡤࡷࡸࡽ࡯ࡳࡦࠪ᝽"),
  bstack11l1l11_opy_ (u"ࠨ࡭ࡨࡽࡆࡲࡩࡢࡵࠪ᝾"), bstack11l1l11_opy_ (u"ࠩ࡮ࡩࡾࡖࡡࡴࡵࡺࡳࡷࡪࠧ᝿"),
  bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࠬក"), bstack11l1l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡄࡶ࡬ࡹࠧខ"), bstack11l1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࡄࡪࡴࠪគ"), bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡈ࡮ࡲࡰ࡯ࡨࡑࡦࡶࡰࡪࡰࡪࡊ࡮ࡲࡥࠨឃ"), bstack11l1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷ࡛ࡳࡦࡕࡼࡷࡹ࡫࡭ࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫង"),
  bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࠫច"), bstack11l1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡑࡱࡵࡸࡸ࠭ឆ"),
  bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡆ࡬ࡷࡦࡨ࡬ࡦࡄࡸ࡭ࡱࡪࡃࡩࡧࡦ࡯ࠬជ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࡖ࡬ࡱࡪࡵࡵࡵࠩឈ"),
  bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡆࡩࡴࡪࡱࡱࠫញ"), bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡉࡡࡵࡧࡪࡳࡷࡿࠧដ"), bstack11l1l11_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡆ࡭ࡣࡪࡷࠬឋ"), bstack11l1l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࡌࡲࡹ࡫࡮ࡵࡃࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫឌ"),
  bstack11l1l11_opy_ (u"ࠩࡧࡳࡳࡺࡓࡵࡱࡳࡅࡵࡶࡏ࡯ࡔࡨࡷࡪࡺࠧឍ"),
  bstack11l1l11_opy_ (u"ࠪࡹࡳ࡯ࡣࡰࡦࡨࡏࡪࡿࡢࡰࡣࡵࡨࠬណ"), bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡎࡩࡾࡨ࡯ࡢࡴࡧࠫត"),
  bstack11l1l11_opy_ (u"ࠬࡴ࡯ࡔ࡫ࡪࡲࠬថ"),
  bstack11l1l11_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࡛࡮ࡪ࡯ࡳࡳࡷࡺࡡ࡯ࡶ࡙࡭ࡪࡽࡳࠨទ"),
  bstack11l1l11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰࡧࡶࡴ࡯ࡤࡘࡣࡷࡧ࡭࡫ࡲࡴࠩធ"),
  bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨន"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡨࡸࡥࡢࡶࡨࡇ࡭ࡸ࡯࡮ࡧࡇࡶ࡮ࡼࡥࡳࡕࡨࡷࡸ࡯࡯࡯ࡵࠪប"),
  bstack11l1l11_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩផ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡑࡣࡷ࡬ࠬព"),
  bstack11l1l11_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰ࡙ࡰࡦࡧࡧࠫភ"),
  bstack11l1l11_opy_ (u"࠭ࡧࡱࡵࡈࡲࡦࡨ࡬ࡦࡦࠪម"),
  bstack11l1l11_opy_ (u"ࠧࡪࡵࡋࡩࡦࡪ࡬ࡦࡵࡶࠫយ"),
  bstack11l1l11_opy_ (u"ࠨࡣࡧࡦࡊࡾࡥࡤࡖ࡬ࡱࡪࡵࡵࡵࠩរ"),
  bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࡕࡦࡶ࡮ࡶࡴࠨល"),
  bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡅࡧࡹ࡭ࡨ࡫ࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧវ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰࡉࡵࡥࡳࡺࡐࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠫឝ"),
  bstack11l1l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡔࡡࡵࡷࡵࡥࡱࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪឞ"),
  bstack11l1l11_opy_ (u"࠭ࡳࡺࡵࡷࡩࡲࡖ࡯ࡳࡶࠪស"),
  bstack11l1l11_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡁࡥࡤࡋࡳࡸࡺࠧហ"),
  bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡛࡮࡭ࡱࡦ࡯ࠬឡ"), bstack11l1l11_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡖࡼࡴࡪ࠭អ"), bstack11l1l11_opy_ (u"ࠪࡹࡳࡲ࡯ࡤ࡭ࡎࡩࡾ࠭ឣ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰࡎࡤࡹࡳࡩࡨࠨឤ"),
  bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡩࡡࡵࡅࡤࡴࡹࡻࡲࡦࠩឥ"),
  bstack11l1l11_opy_ (u"࠭ࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࡑࡷ࡬ࡪࡸࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨឦ"),
  bstack11l1l11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡘ࡫ࡱࡨࡴࡽࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࠩឧ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡰࡱ࡯ࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬឨ"),
  bstack11l1l11_opy_ (u"ࠩࡨࡲ࡫ࡵࡲࡤࡧࡄࡴࡵࡏ࡮ࡴࡶࡤࡰࡱ࠭ឩ"),
  bstack11l1l11_opy_ (u"ࠪࡩࡳࡹࡵࡳࡧ࡚ࡩࡧࡼࡩࡦࡹࡶࡌࡦࡼࡥࡑࡣࡪࡩࡸ࠭ឪ"), bstack11l1l11_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡉ࡫ࡶࡵࡱࡲࡰࡸࡖ࡯ࡳࡶࠪឫ"), bstack11l1l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡉ࡫ࡴࡢ࡫࡯ࡷࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠨឬ"),
  bstack11l1l11_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡰࡱࡵࡆࡥࡨ࡮ࡥࡍ࡫ࡰ࡭ࡹ࠭ឭ"),
  bstack11l1l11_opy_ (u"ࠧࡤࡣ࡯ࡩࡳࡪࡡࡳࡈࡲࡶࡲࡧࡴࠨឮ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡸࡲࡩࡲࡥࡊࡦࠪឯ"),
  bstack11l1l11_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩឰ"),
  bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ឱ"), bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࡙ࡥࡳࡸ࡬ࡧࡪࡹࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡦࡦࠪឲ"),
  bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡄࡧࡨ࡫ࡰࡵࡃ࡯ࡩࡷࡺࡳࠨឳ"), bstack11l1l11_opy_ (u"࠭ࡡࡶࡶࡲࡈ࡮ࡹ࡭ࡪࡵࡶࡅࡱ࡫ࡲࡵࡵࠪ឴"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡶࡐ࡮ࡨࠧ឵"),
  bstack11l1l11_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡘࡦࡶࠧា"),
  bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡱ࡭ࡹ࡯ࡡ࡭ࡗࡵࡰࠬិ"), bstack11l1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡄࡰࡱࡵࡷࡑࡱࡳࡹࡵࡹࠧី"), bstack11l1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍ࡬ࡴ࡯ࡳࡧࡉࡶࡦࡻࡤࡘࡣࡵࡲ࡮ࡴࡧࠨឹ"), bstack11l1l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡥ࡯ࡎ࡬ࡲࡰࡹࡉ࡯ࡄࡤࡧࡰ࡭ࡲࡰࡷࡱࡨࠬឺ"),
  bstack11l1l11_opy_ (u"࠭࡫ࡦࡧࡳࡏࡪࡿࡃࡩࡣ࡬ࡲࡸ࠭ុ"),
  bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡺࡢࡤ࡯ࡩࡘࡺࡲࡪࡰࡪࡷࡉ࡯ࡲࠨូ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡨ࡫ࡳࡴࡃࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫួ"),
  bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲࡌࡧࡼࡈࡪࡲࡡࡺࠩើ"),
  bstack11l1l11_opy_ (u"ࠪࡷ࡭ࡵࡷࡊࡑࡖࡐࡴ࡭ࠧឿ"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ៀ"),
  bstack11l1l11_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡗ࡫ࡳࡱࡱࡱࡷࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭េ"), bstack11l1l11_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶ࡚ࡥ࡮ࡺࡔࡪ࡯ࡨࡳࡺࡺࠧែ"),
  bstack11l1l11_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࠪៃ"),
  bstack11l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡵࡼࡲࡨࡋࡸࡦࡥࡸࡸࡪࡌࡲࡰ࡯ࡋࡸࡹࡶࡳࠨោ"),
  bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡆࡥࡵࡺࡵࡳࡧࠪៅ"),
  bstack11l1l11_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪំ"),
  bstack11l1l11_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡅࡲࡲࡹ࡫ࡸࡵࡎ࡬ࡷࡹ࠭ះ"),
  bstack11l1l11_opy_ (u"ࠬࡽࡡࡪࡶࡉࡳࡷࡇࡰࡱࡕࡦࡶ࡮ࡶࡴࠨៈ"),
  bstack11l1l11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡃࡰࡰࡱࡩࡨࡺࡒࡦࡶࡵ࡭ࡪࡹࠧ៉"),
  bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡒࡦࡳࡥࠨ៊"),
  bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡕࡏࡇࡪࡸࡴࠨ់"),
  bstack11l1l11_opy_ (u"ࠩࡷࡥࡵ࡝ࡩࡵࡪࡖ࡬ࡴࡸࡴࡑࡴࡨࡷࡸࡊࡵࡳࡣࡷ࡭ࡴࡴࠧ៌"),
  bstack11l1l11_opy_ (u"ࠪࡷࡨࡧ࡬ࡦࡈࡤࡧࡹࡵࡲࠨ៍"),
  bstack11l1l11_opy_ (u"ࠫࡼࡪࡡࡍࡱࡦࡥࡱࡖ࡯ࡳࡶࠪ៎"),
  bstack11l1l11_opy_ (u"ࠬࡹࡨࡰࡹ࡛ࡧࡴࡪࡥࡍࡱࡪࠫ៏"),
  bstack11l1l11_opy_ (u"࠭ࡩࡰࡵࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡺࡹࡥࠨ័"),
  bstack11l1l11_opy_ (u"ࠧࡹࡥࡲࡨࡪࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠩ៑"),
  bstack11l1l11_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡸࡹࡷࡰࡴࡧ្ࠫ"),
  bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡖࡲࡦࡤࡸ࡭ࡱࡺࡗࡅࡃࠪ៓"),
  bstack11l1l11_opy_ (u"ࠪࡴࡷ࡫ࡶࡦࡰࡷ࡛ࡉࡇࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠫ។"),
  bstack11l1l11_opy_ (u"ࠫࡼ࡫ࡢࡅࡴ࡬ࡺࡪࡸࡁࡨࡧࡱࡸ࡚ࡸ࡬ࠨ៕"),
  bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡶ࡫ࠫ៖"),
  bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡑࡩࡼ࡝ࡄࡂࠩៗ"),
  bstack11l1l11_opy_ (u"ࠧࡸࡦࡤࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪ៘"), bstack11l1l11_opy_ (u"ࠨࡹࡧࡥࡈࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࡕ࡫ࡰࡩࡴࡻࡴࠨ៙"),
  bstack11l1l11_opy_ (u"ࠩࡻࡧࡴࡪࡥࡐࡴࡪࡍࡩ࠭៚"), bstack11l1l11_opy_ (u"ࠪࡼࡨࡵࡤࡦࡕ࡬࡫ࡳ࡯࡮ࡨࡋࡧࠫ៛"),
  bstack11l1l11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨ࡜ࡊࡁࡃࡷࡱࡨࡱ࡫ࡉࡥࠩៜ"),
  bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡧࡷࡓࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡴࡷࡓࡳࡲࡹࠨ៝"),
  bstack11l1l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࡳࠨ៞"),
  bstack11l1l11_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡪࡧࡶࠫ៟"), bstack11l1l11_opy_ (u"ࠨࡹࡧࡥࡘࡺࡡࡳࡶࡸࡴࡗ࡫ࡴࡳࡻࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠫ០"),
  bstack11l1l11_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࡋࡥࡷࡪࡷࡢࡴࡨࡏࡪࡿࡢࡰࡣࡵࡨࠬ១"),
  bstack11l1l11_opy_ (u"ࠪࡱࡦࡾࡔࡺࡲ࡬ࡲ࡬ࡌࡲࡦࡳࡸࡩࡳࡩࡹࠨ២"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡯࡭ࡱ࡮ࡨࡍࡸ࡜ࡩࡴ࡫ࡥࡰࡪࡉࡨࡦࡥ࡮ࠫ៣"),
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡅࡤࡶࡹ࡮ࡡࡨࡧࡖࡷࡱ࠭៤"),
  bstack11l1l11_opy_ (u"࠭ࡳࡩࡱࡸࡰࡩ࡛ࡳࡦࡕ࡬ࡲ࡬ࡲࡥࡵࡱࡱࡘࡪࡹࡴࡎࡣࡱࡥ࡬࡫ࡲࠨ៥"),
  bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹࡏࡗࡅࡒࠪ៦"),
  bstack11l1l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡔࡰࡷࡦ࡬ࡎࡪࡅ࡯ࡴࡲࡰࡱ࠭៧"),
  bstack11l1l11_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡊ࡬ࡨࡩ࡫࡮ࡂࡲ࡬ࡔࡴࡲࡩࡤࡻࡈࡶࡷࡵࡲࠨ៨"),
  bstack11l1l11_opy_ (u"ࠪࡱࡴࡩ࡫ࡍࡱࡦࡥࡹ࡯࡯࡯ࡃࡳࡴࠬ៩"),
  bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊࡴࡸ࡭ࡢࡶࠪ៪"), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡥࡤࡸࡋ࡯࡬ࡵࡧࡵࡗࡵ࡫ࡣࡴࠩ៫"),
  bstack11l1l11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡉ࡫࡬ࡢࡻࡄࡨࡧ࠭៬"),
  bstack11l1l11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡊࡦࡏࡳࡨࡧࡴࡰࡴࡄࡹࡹࡵࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠪ៭")
]
bstack11llll1l11_opy_ = bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡶࡲ࡯ࡳࡦࡪࠧ៮")
bstack11llll11l_opy_ = [bstack11l1l11_opy_ (u"ࠩ࠱ࡥࡵࡱࠧ៯"), bstack11l1l11_opy_ (u"ࠪ࠲ࡦࡧࡢࠨ៰"), bstack11l1l11_opy_ (u"ࠫ࠳࡯ࡰࡢࠩ៱")]
bstack1llll1111_opy_ = [bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨ៲"), bstack11l1l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ៳"), bstack11l1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ៴"), bstack11l1l11_opy_ (u"ࠨࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪࠧ៵")]
bstack1l11ll1l_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៶"): bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៷"),
  bstack11l1l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ៸"): bstack11l1l11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ៹"),
  bstack11l1l11_opy_ (u"࠭ࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ៺"): bstack11l1l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៻"),
  bstack11l1l11_opy_ (u"ࠨ࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ៼"): bstack11l1l11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៽"),
  bstack11l1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡹ࡯࡯࡯ࡵࠪ៾"): bstack11l1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ៿")
}
bstack1lll11111l_opy_ = [
  bstack11l1l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᠀"),
  bstack11l1l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ᠁"),
  bstack11l1l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᠂"),
  bstack11l1l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠃"),
  bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ᠄"),
]
bstack1ll111l11l_opy_ = bstack1l1lll11ll_opy_ + bstack11llll111l1_opy_ + bstack11ll11l1_opy_
bstack1llll1ll11_opy_ = [
  bstack11l1l11_opy_ (u"ࠪࡢࡱࡵࡣࡢ࡮࡫ࡳࡸࡺࠤࠨ᠅"),
  bstack11l1l11_opy_ (u"ࠫࡣࡨࡳ࠮࡮ࡲࡧࡦࡲ࠮ࡤࡱࡰࠨࠬ᠆"),
  bstack11l1l11_opy_ (u"ࠬࡤ࠱࠳࠹࠱ࠫ᠇"),
  bstack11l1l11_opy_ (u"࠭࡞࠲࠲࠱ࠫ᠈"),
  bstack11l1l11_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠷࡛࠷࠯࠼ࡡ࠳࠭᠉"),
  bstack11l1l11_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠲࡜࠲࠰࠽ࡢ࠴ࠧ᠊"),
  bstack11l1l11_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠴࡝࠳࠱࠶ࡣ࠮ࠨ᠋"),
  bstack11l1l11_opy_ (u"ࠪࡢ࠶࠿࠲࠯࠳࠹࠼࠳࠭᠌")
]
bstack11lll1lll1l_opy_ = bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ᠍")
bstack1l11ll11l_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴࡫ࡶࡦࡰࡷࠫ᠎")
bstack11l11l111_opy_ = [ bstack11l1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᠏") ]
bstack1l11l1l11l_opy_ = [ bstack11l1l11_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᠐") ]
bstack1lll1ll1_opy_ = [bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᠑")]
bstack1l11l11lll_opy_ = [ bstack11l1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᠒") ]
bstack1lll1lllll_opy_ = bstack11l1l11_opy_ (u"ࠪࡗࡉࡑࡓࡦࡶࡸࡴࠬ᠓")
bstack11l1l11l1_opy_ = bstack11l1l11_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧ᠔")
bstack11l1l111_opy_ = bstack11l1l11_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹ࡙ࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠩ᠕")
bstack11lllll11_opy_ = bstack11l1l11_opy_ (u"࠭࠴࠯࠲࠱࠴ࠬ᠖")
bstack1111lll11_opy_ = [
  bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡣࡋࡇࡉࡍࡇࡇࠫ᠗"),
  bstack11l1l11_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨ᠘"),
  bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡥࡂࡍࡑࡆࡏࡊࡊ࡟ࡃ࡛ࡢࡇࡑࡏࡅࡏࡖࠪ᠙"),
  bstack11l1l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡇࡗ࡛ࡔࡘࡋࡠࡅࡋࡅࡓࡍࡅࡅࠩ᠚"),
  bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐࡋࡔࡠࡐࡒࡘࡤࡉࡏࡏࡐࡈࡇ࡙ࡋࡄࠨ᠛"),
  bstack11l1l11_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡃࡍࡑࡖࡉࡉ࠭᠜"),
  bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡖࡉ࡙࠭᠝"),
  bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡔࡈࡊ࡚࡙ࡅࡅࠩ᠞"),
  bstack11l1l11_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡄࡆࡔࡘࡔࡆࡆࠪ᠟"),
  bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᠠ"),
  bstack11l1l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫᠡ"),
  bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡌࡒ࡛ࡇࡌࡊࡆࠪᠢ"),
  bstack11l1l11_opy_ (u"ࠬࡋࡒࡓࡡࡄࡈࡉࡘࡅࡔࡕࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨᠣ"),
  bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡢࡘ࡚ࡔࡎࡆࡎࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᠤ"),
  bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫᠥ"),
  bstack11l1l11_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᠦ"),
  bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡗࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡋࡓࡘ࡚࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬᠧ"),
  bstack11l1l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡑࡔࡒ࡜࡞ࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᠨ"),
  bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬᠩ"),
  bstack11l1l11_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡓࡇࡖࡓࡑ࡛ࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᠪ"),
  bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡢࡑࡆࡔࡄࡂࡖࡒࡖ࡞ࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᠫ"),
]
bstack1ll1lll111_opy_ = bstack11l1l11_opy_ (u"ࠧ࠯࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡣࡵࡸ࡮࡬ࡡࡤࡶࡶ࠳ࠬᠬ")
bstack1ll1l11ll1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪᠭ")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᠮ"), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᠯ"))
bstack1l111l11l1l_opy_ = bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡳ࡭ࠬᠰ")
bstack11llll1llll_opy_ = [ bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᠱ"), bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᠲ"), bstack11l1l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ᠳ"), bstack11l1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨᠴ")]
bstack1l1111lll_opy_ = [ bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᠵ"), bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᠶ"), bstack11l1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪᠷ"), bstack11l1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᠸ") ]
bstack1l11lllll1_opy_ = [ bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᠹ") ]
bstack1l1lll111l_opy_ = 360
bstack1l11111lll1_opy_ = bstack11l1l11_opy_ (u"ࠢࡢࡲࡳ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᠺ")
bstack11llll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵࠥᠻ")
bstack11llll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠧᠼ")
bstack1l1111ll111_opy_ = bstack11l1l11_opy_ (u"ࠥࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡹ࡫ࡳࡵࡵࠣࡥࡷ࡫ࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡏࡔࠢࡹࡩࡷࡹࡩࡰࡰࠣࠩࡸࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦࠢࡩࡳࡷࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠࡥࡧࡹ࡭ࡨ࡫ࡳ࠯ࠤᠽ")
bstack1l111l1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠦ࠶࠷࠮࠱ࠤᠾ")
bstack111lll11l1_opy_ = {
  bstack11l1l11_opy_ (u"ࠬࡖࡁࡔࡕࠪᠿ"): bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᡀ"),
  bstack11l1l11_opy_ (u"ࠧࡇࡃࡌࡐࠬᡁ"): bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᡂ"),
  bstack11l1l11_opy_ (u"ࠩࡖࡏࡎࡖࠧᡃ"): bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᡄ")
}
bstack11ll111l1l_opy_ = [
  bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࠣᡅ"),
  bstack11l1l11_opy_ (u"ࠧ࡭࡯ࡃࡣࡦ࡯ࠧᡆ"),
  bstack11l1l11_opy_ (u"ࠨࡧࡰࡈࡲࡶࡼࡧࡲࡥࠤᡇ"),
  bstack11l1l11_opy_ (u"ࠢࡳࡧࡩࡶࡪࡹࡨࠣᡈ"),
  bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᡉ"),
  bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᡊ"),
  bstack11l1l11_opy_ (u"ࠥࡷࡺࡨ࡭ࡪࡶࡈࡰࡪࡳࡥ࡯ࡶࠥᡋ"),
  bstack11l1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣᡌ"),
  bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣᡍ"),
  bstack11l1l11_opy_ (u"ࠨࡣ࡭ࡧࡤࡶࡊࡲࡥ࡮ࡧࡱࡸࠧᡎ"),
  bstack11l1l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࡳࠣᡏ"),
  bstack11l1l11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠣᡐ"),
  bstack11l1l11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡄࡷࡾࡴࡣࡔࡥࡵ࡭ࡵࡺࠢᡑ"),
  bstack11l1l11_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᡒ"),
  bstack11l1l11_opy_ (u"ࠦࡶࡻࡩࡵࠤᡓ"),
  bstack11l1l11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲ࡚࡯ࡶࡥ࡫ࡅࡨࡺࡩࡰࡰࠥᡔ"),
  bstack11l1l11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡍࡶ࡮ࡷ࡭࡙ࡵࡵࡤࡪࠥᡕ"),
  bstack11l1l11_opy_ (u"ࠢࡴࡪࡤ࡯ࡪࠨᡖ"),
  bstack11l1l11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࡁࡱࡲࠥᡗ")
]
bstack11lllllll1l_opy_ = [
  bstack11l1l11_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣᡘ"),
  bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᡙ"),
  bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡰࠤᡚ"),
  bstack11l1l11_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧᡛ"),
  bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᡜ")
]
bstack1lllll111l_opy_ = {
  bstack11l1l11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᡝ"): [bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᡞ")],
  bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᡟ"): [bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᡠ")],
  bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡰࠤᡡ"): [bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤᡢ"), bstack11l1l11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤᡣ"), bstack11l1l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᡤ"), bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᡥ")],
  bstack11l1l11_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤᡦ"): [bstack11l1l11_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥᡧ")],
  bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᡨ"): [bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᡩ")],
}
bstack11lllll1111_opy_ = {
  bstack11l1l11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧᡪ"): bstack11l1l11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᡫ"),
  bstack11l1l11_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᡬ"): bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᡭ"),
  bstack11l1l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢᡮ"): bstack11l1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨᡯ"),
  bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣᡰ"): bstack11l1l11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣᡱ"),
  bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᡲ"): bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᡳ")
}
bstack111lll1lll_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᡴ"): bstack11l1l11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡖࡩࡹࡻࡰࠨᡵ"),
  bstack11l1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᡶ"): bstack11l1l11_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ᡷ"),
  bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᡸ"): bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸ࡙ࠥࡥࡵࡷࡳࠫ᡹"),
  bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ᡺"): bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩ᡻")
}
bstack11lllllll11_opy_ = 65536
bstack11llllll11l_opy_ = bstack11l1l11_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫ᡼")
bstack11llll1ll11_opy_ = [
      bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᡽"), bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᡾"), bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᡿"), bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᢀ"), bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᢁ"),
      bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᢂ"), bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᢃ"), bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᢄ"), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᢅ"),
      bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᢆ"), bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᢇ"), bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᢈ")
    ]
bstack11lll1llll1_opy_= {
  bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᢉ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᢊ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᢋ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢌ"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᢍ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᢎ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᢏ"): bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᢐ"),
  bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᢑ"): bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᢒ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᢓ"): bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᢔ"),
  bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᢕ"): bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᢖ"),
  bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᢗ"): bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᢘ"),
  bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᢙ"): bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᢚ"),
  bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᢛ"): bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬᢜ"),
  bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᢝ"): bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᢞ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᢟ"): bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᢠ"),
  bstack11l1l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᢡ"): bstack11l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨᢢ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᢣ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᢤ"),
  bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᢥ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᢦ"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᢧ"): bstack11l1l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᢨ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽᢩࠬ"): bstack11l1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᢪ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᢫"): bstack11l1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᢬"),
  bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭᢭"): bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ᢮"),
  bstack11l1l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ᢯"): bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᢰ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᢱ"): bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᢲ"),
  bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢳ"): bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᢴ"),
  bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᢵ"): bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᢶ"),
  bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᢷ"): bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫᢸ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᢹ"): bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᢺ")
}
bstack11lllll1ll1_opy_ = [bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᢻ"), bstack11l1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᢼ")]
bstack1l1111llll_opy_ = (bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᢽ"),)
bstack11llll11lll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡵࡱࡦࡤࡸࡪࡥࡣ࡭࡫ࠪᢾ")
bstack1ll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲࡫ࡷ࡯ࡤࡴ࠱ࠥᢿ")
bstack11l1l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡪࡶ࡮ࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡦࡹࡨࡣࡱࡤࡶࡩ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࠢᣀ")
bstack1ll1111ll1_opy_ = bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠥᣁ")
class EVENTS(Enum):
  bstack11lll1lllll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧᣂ")
  bstack11lll1ll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯ࡩࡦࡴࡵࡱࠩᣃ") # final bstack11lllll11l1_opy_
  bstack11lllll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࡬ࡰࡩࡶࠫᣄ")
  bstack11ll11l1l1_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩᣅ") #shift post bstack11lllll1lll_opy_
  bstack11lll11lll_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨᣆ") #shift post bstack11lllll1lll_opy_
  bstack11llll1l111_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶ࡫ࡹࡧ࠭ᣇ") #shift
  bstack11lllll11ll_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧᣈ") #shift
  bstack1lll1l111l_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬᣉ")
  bstack1ll1l1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡳࡢࡸࡨ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬᣊ")
  bstack1l111l1l11_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡱࡧࡵࡪࡴࡸ࡭ࡴࡥࡤࡲࠬᣋ")
  bstack1l11111ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡲ࡯ࡤࡣ࡯ࠫᣌ") #shift
  bstack11lllll1ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡥࡵࡶ࠭ࡶࡲ࡯ࡳࡦࡪࠧᣍ") #shift
  bstack11ll1l111_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡤ࡫࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠭ᣎ")
  bstack1lll1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᣏ") #shift
  bstack1ll1l1lll1_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪᣐ") #shift
  bstack11llll11l1l_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿࠧᣑ") #shift
  bstack1l1lll1llll_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᣒ")
  bstack1ll1l1l1l_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡳࡵࡣࡷࡹࡸ࠭ᣓ") #shift
  bstack1l11111l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧᣔ")
  bstack11lllll111l_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡺࡼ࠱ࡸ࡫ࡴࡶࡲࠪᣕ") #shift
  bstack1l1l11l1l1_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡶࡸࡴࠬᣖ")
  bstack11llllll111_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳ࡯ࡣࡳࡷ࡭ࡵࡴࠨᣗ") # not bstack11llll1l1ll_opy_ in python
  bstack11l1ll1l11_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡳࡸ࡭ࡹ࠭ᣘ") # used in bstack11llllll1ll_opy_
  bstack11lll1l111_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡪࡩࡹ࠭ᣙ") # used in bstack11llllll1ll_opy_
  bstack1lll1ll1ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽࡬ࡴࡵ࡫ࠨᣚ")
  bstack11l1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠬᣛ")
  bstack1l1111111_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠬᣜ") #
  bstack1l1lllll1l_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬᣝ")
  bstack1ll1l1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬᣞ")
  bstack1111ll111_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪᣟ")
  bstack1ll1ll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬᣠ")
  bstack1ll1lll1ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᣡ") #shift
  bstack111ll111l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᣢ") #shift
  bstack11llllllll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫᣣ")
  bstack11llll1lll1_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧᣤ")
  bstack1llll1l11l1_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡸࡺࡡࡳࡶࠪᣥ")
  bstack11llll1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧᣦ")
  bstack11llll111ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡣࡩࡧࡦ࡯࠲ࡻࡰࡥࡣࡷࡩࠬᣧ")
  bstack1lll1111ll1_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠭ᣨ")
  bstack1lll11l111l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡨࡵ࡮࡯ࡧࡦࡸࠬᣩ")
  bstack1lll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡹࡴࡰࡲࠪᣪ")
  bstack1llllllll11_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡳࡵࡣࡵࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࠨᣫ")
  bstack1lll1ll11l1_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱࠫᣬ")
  bstack11llll1l11l_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠬᣭ")
  bstack11llllll1l1_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡩ࡭ࡳࡪࡎࡦࡣࡵࡩࡸࡺࡈࡶࡤࠪᣮ")
  bstack1l1l1l1ll11_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡋࡱ࡭ࡹ࠭ᣯ")
  bstack1l1l1lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡸࡴࠨᣰ")
  bstack1ll1l1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫᣱ")
  bstack11lllllllll_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡉ࡯࡯ࡨ࡬࡫ࠬᣲ")
  bstack1ll11ll1lll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡗࡹ࡫ࡰࠨᣳ")
  bstack1ll11lllll1_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࡬ࡗࡪࡲࡦࡉࡧࡤࡰࡌ࡫ࡴࡓࡧࡶࡹࡱࡺࠧᣴ")
  bstack1ll11l1111l_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡇࡹࡩࡳࡺࠧᣵ")
  bstack1l1llll11ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹ࠭᣶")
  bstack1ll111l1lll_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻࡮ࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࡊࡼࡥ࡯ࡶࠪ᣷")
  bstack11lll1lll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡨࡲࡶࡻࡥࡶࡧࡗࡩࡸࡺࡅࡷࡧࡱࡸࠬ᣸")
  bstack1l1l1l1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺ࡯ࡱࠩ᣹")
  bstack1lll1lll1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡰࡰࡖࡸࡴࡶࠧ᣺")
class STAGE(Enum):
  bstack1ll11l11ll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ᣻")
  END = bstack11l1l11_opy_ (u"ࠬ࡫࡮ࡥࠩ᣼")
  bstack1l1ll1lll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡪࡰࡪࡰࡪ࠭᣽")
bstack1l1111l1l1_opy_ = {
  bstack11l1l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧ᣾"): bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᣿"),
  bstack11l1l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ᤀ"): bstack11l1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᤁ")
}
PLAYWRIGHT_HUB_URL = bstack11l1l11_opy_ (u"ࠦࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂࠨᤂ")