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
import os
import json
import shutil
import tempfile
import threading
import urllib.request
import uuid
from pathlib import Path
import logging
import re
from bstack_utils.helper import bstack1ll1111ll11_opy_
bstack1l11111l1ll_opy_ = 100 * 1024 * 1024 # 100 bstack1l11111llll_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1lll11l1l_opy_ = bstack1ll1111ll11_opy_()
bstack1l1lllll111_opy_ = bstack1ll1l1_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᔨ")
bstack1l111l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᔩ")
bstack1l111l1l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᔪ")
bstack1l111l1l11l_opy_ = bstack1ll1l1_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᔫ")
bstack11llllllll1_opy_ = bstack1ll1l1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᔬ")
_1l1111111l1_opy_ = threading.local()
def bstack1l111ll111l_opy_(test_framework_state, test_hook_state):
    bstack1ll1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡥࡩࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡶ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࠮ࡳࡶࡥ࡫ࠤࡦࡹࠠࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠮ࠐࠠࠡࠢࠣࡦࡪ࡬࡯ࡳࡧࠣࡥࡳࡿࠠࡧ࡫࡯ࡩࠥࡻࡰ࡭ࡱࡤࡨࡸࠦ࡯ࡤࡥࡸࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᔭ")
    _1l1111111l1_opy_.test_framework_state = test_framework_state
    _1l1111111l1_opy_.test_hook_state = test_hook_state
def bstack1l11111111l_opy_():
    bstack1ll1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡗ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡳࡧࡤࡨ࠲ࡲ࡯ࡤࡣ࡯ࠤࡸࡺ࡯ࡳࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦࡴࡶࡲ࡯ࡩࠥ࠮ࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪ࠲ࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࠫࠣࡳࡷࠦࠨࡏࡱࡱࡩ࠱ࠦࡎࡰࡰࡨ࠭ࠥ࡯ࡦࠡࡰࡲࡸࠥࡹࡥࡵ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᔮ")
    return (
        getattr(_1l1111111l1_opy_, bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࠬᔯ"), None),
        getattr(_1l1111111l1_opy_, bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠨᔰ"), None)
    )
class bstack11lll1ll_opy_:
    bstack1ll1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡇ࡫࡯ࡩ࡚ࡶ࡬ࡰࡣࡧࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࡤࡰ࡮ࡺࡹࠡࡶࡲࠤࡺࡶ࡬ࡰࡣࡧࠤࡦࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࡍࡹࠦࡳࡶࡲࡳࡳࡷࡺࡳࠡࡤࡲࡸ࡭ࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢࡤࡲࡩࠦࡈࡕࡖࡓ࠳ࡍ࡚ࡔࡑࡕ࡙ࠣࡗࡒࡳ࠭ࠢࡤࡲࡩࠦࡣࡰࡲ࡬ࡩࡸࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡ࡫ࡱࡸࡴࠦࡡࠡࡦࡨࡷ࡮࡭࡮ࡢࡶࡨࡨࠏࠦࠠࠡࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡽࡩࡵࡪ࡬ࡲࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢ࡫ࡳࡲ࡫ࠠࡧࡱ࡯ࡨࡪࡸࠠࡶࡰࡧࡩࡷࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࡏࡦࠡࡣࡱࠤࡴࡶࡴࡪࡱࡱࡥࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࠦࠨࡪࡰࠣࡎࡘࡕࡎࠡࡨࡲࡶࡲࡧࡴࠪࠢ࡬ࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡢࡰࡧࠤࡨࡵ࡮ࡵࡣ࡬ࡲࡸࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࠣࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡱࡥࡺࠢࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ࠲ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡴࡱࡧࡣࡦࡦࠣ࡭ࡳࠦࡴࡩࡧࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡩࡳࡱࡪࡥࡳ࠽ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪ࠲ࠊࠡࠢࠣࠤ࡮ࡺࠠࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡮ࡹࠠࡢࠢࡹࡳ࡮ࡪࠠ࡮ࡧࡷ࡬ࡴࡪ⠔ࡪࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡶࠤࡦࡲ࡬ࠡࡧࡵࡶࡴࡸࡳࠡࡩࡵࡥࡨ࡫ࡦࡶ࡮࡯ࡽࠥࡨࡹࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡴࡩࡧࡰࠤࡦࡴࡤࠡࡵ࡬ࡱࡵࡲࡹࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡺࡨࡳࡱࡺ࡭ࡳ࡭ࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᔱ")
    @staticmethod
    def upload_attachment(bstack1l111111111_opy_: str, *bstack1l111111ll1_opy_) -> None:
        if not bstack1l111111111_opy_ or not bstack1l111111111_opy_.strip():
            logger.error(bstack1ll1l1_opy_ (u"ࠣࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡔࡷࡵࡶࡪࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡ࡫ࡶࠤࡪࡳࡰࡵࡻࠣࡳࡷࠦࡎࡰࡰࡨ࠲ࠧᔲ"))
            return
        bstack1l11111l111_opy_ = bstack1l111111ll1_opy_[0] if bstack1l111111ll1_opy_ and len(bstack1l111111ll1_opy_) > 0 else None
        bstack1l111111lll_opy_ = None
        test_framework_state, test_hook_state = bstack1l11111111l_opy_()
        try:
            if bstack1l111111111_opy_.startswith(bstack1ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᔳ")) or bstack1l111111111_opy_.startswith(bstack1ll1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᔴ")):
                logger.debug(bstack1ll1l1_opy_ (u"ࠦࡕࡧࡴࡩࠢ࡬ࡷࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡥࠢࡤࡷ࡛ࠥࡒࡍ࠽ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠦᔵ"))
                url = bstack1l111111111_opy_
                bstack1l11111l11l_opy_ = str(uuid.uuid4())
                bstack1l11111ll1l_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack1l11111ll1l_opy_ or not bstack1l11111ll1l_opy_.strip():
                    bstack1l11111ll1l_opy_ = bstack1l11111l11l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1ll1l1_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡤࠨᔶ") + bstack1l11111l11l_opy_ + bstack1ll1l1_opy_ (u"ࠨ࡟ࠣᔷ"),
                                                        suffix=bstack1ll1l1_opy_ (u"ࠢࡠࠤᔸ") + bstack1l11111ll1l_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1ll1l1_opy_ (u"ࠨࡹࡥࠫᔹ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1l111111lll_opy_ = Path(temp_file.name)
                logger.debug(bstack1ll1l1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡰࡴࡩࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᔺ").format(bstack1l111111lll_opy_))
            else:
                bstack1l111111lll_opy_ = Path(bstack1l111111111_opy_)
                logger.debug(bstack1ll1l1_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧᔻ").format(bstack1l111111lll_opy_))
        except Exception as e:
            logger.error(bstack1ll1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡰࡤࡷࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥ࡬ࡲࡰ࡯ࠣࡴࡦࡺࡨ࠰ࡗࡕࡐ࠿ࠦࡻࡾࠤᔼ").format(e))
            return
        if bstack1l111111lll_opy_ is None or not bstack1l111111lll_opy_.exists():
            logger.error(bstack1ll1l1_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᔽ").format(bstack1l111111lll_opy_))
            return
        if bstack1l111111lll_opy_.stat().st_size > bstack1l11111l1ll_opy_:
            logger.error(bstack1ll1l1_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸ࡯ࡺࡦࠢࡨࡼࡨ࡫ࡥࡥࡵࠣࡱࡦࡾࡩ࡮ࡷࡰࠤࡦࡲ࡬ࡰࡹࡨࡨࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡻࡾࠤᔾ").format(bstack1l11111l1ll_opy_))
            return
        bstack1l1111111ll_opy_ = bstack1ll1l1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᔿ")
        if bstack1l11111l111_opy_:
            try:
                params = json.loads(bstack1l11111l111_opy_)
                if bstack1ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᕀ") in params and params.get(bstack1ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᕁ")) is True:
                    bstack1l1111111ll_opy_ = bstack1ll1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᕂ")
            except Exception as bstack1l111111l11_opy_:
                logger.error(bstack1ll1l1_opy_ (u"ࠦࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡒࡤࡶࡦࡳࡳ࠻ࠢࡾࢁࠧᕃ").format(bstack1l111111l11_opy_))
        bstack1l11111l1l1_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1llll11l111_opy_
        if test_framework_state in bstack1llll11l111_opy_.bstack1l11ll111l1_opy_:
            if bstack1l1111111ll_opy_ == bstack1l111l1l1l1_opy_:
                bstack1l11111l1l1_opy_ = True
            bstack1l1111111ll_opy_ = bstack1l111l1l11l_opy_
        try:
            platform_index = os.environ[bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᕄ")]
            target_dir = os.path.join(bstack1l1lll11l1l_opy_, bstack1l1lllll111_opy_ + str(platform_index),
                                      bstack1l1111111ll_opy_)
            if bstack1l11111l1l1_opy_:
                target_dir = os.path.join(target_dir, bstack11llllllll1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1ll1l1_opy_ (u"ࠨࡃࡳࡧࡤࡸࡪࡪ࠯ࡷࡧࡵ࡭࡫࡯ࡥࡥࠢࡷࡥࡷ࡭ࡥࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᕅ").format(target_dir))
            file_name = os.path.basename(bstack1l111111lll_opy_)
            bstack1l11111ll11_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack1l11111ll11_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lllllllll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lllllllll_opy_) + extension)):
                    bstack11lllllllll_opy_ += 1
                bstack1l11111ll11_opy_ = os.path.join(target_dir, base_name + str(bstack11lllllllll_opy_) + extension)
            shutil.copy(bstack1l111111lll_opy_, bstack1l11111ll11_opy_)
            logger.info(bstack1ll1l1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡨࡵࡰࡪࡧࡧࠤࡹࡵ࠺ࠡࡽࢀࠦᕆ").format(bstack1l11111ll11_opy_))
        except Exception as e:
            logger.error(bstack1ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡮ࡱࡹ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥࡺ࡯ࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᕇ").format(e))
            return
        finally:
            if bstack1l111111111_opy_.startswith(bstack1ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᕈ")) or bstack1l111111111_opy_.startswith(bstack1ll1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᕉ")):
                try:
                    if bstack1l111111lll_opy_ is not None and bstack1l111111lll_opy_.exists():
                        bstack1l111111lll_opy_.unlink()
                        logger.debug(bstack1ll1l1_opy_ (u"࡙ࠦ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩࠥࡪࡥ࡭ࡧࡷࡩࡩࡀࠠࡼࡿࠥᕊ").format(bstack1l111111lll_opy_))
                except Exception as ex:
                    logger.error(bstack1ll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦᕋ").format(ex))
    @staticmethod
    def bstack1l1111l11_opy_() -> None:
        bstack1ll1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡪࡲࡥࡵࡧࡶࠤࡦࡲ࡬ࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡺ࡬ࡴࡹࡥࠡࡰࡤࡱࡪࡹࠠࡴࡶࡤࡶࡹࠦࡷࡪࡶ࡫ࠤ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧࠦࡦࡰ࡮࡯ࡳࡼ࡫ࡤࠡࡤࡼࠤࡦࠦ࡮ࡶ࡯ࡥࡩࡷࠦࡩ࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᕌ")
        bstack1l11111lll1_opy_ = bstack1ll1111ll11_opy_()
        pattern = re.compile(bstack1ll1l1_opy_ (u"ࡲࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭࡝ࡦ࠮ࠦᕍ"))
        if os.path.exists(bstack1l11111lll1_opy_):
            for item in os.listdir(bstack1l11111lll1_opy_):
                bstack1l111111l1l_opy_ = os.path.join(bstack1l11111lll1_opy_, item)
                if os.path.isdir(bstack1l111111l1l_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack1l111111l1l_opy_)
                    except Exception as e:
                        logger.error(bstack1ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᕎ").format(e))
        else:
            logger.info(bstack1ll1l1_opy_ (u"ࠤࡗ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᕏ").format(bstack1l11111lll1_opy_))