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
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack1llllllllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll11llll1_opy_(bstack1lll1llll11_opy_):
    bstack1ll1l11ll1l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1ll11lll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11lll111_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11lll11l_opy_(hub_url):
            if not bstack1lll11llll1_opy_.bstack1ll1l11ll1l_opy_:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᅽ") + str(hub_url) + bstack1ll1l1_opy_ (u"ࠧࠨᅾ"))
                bstack1lll11llll1_opy_.bstack1ll1l11ll1l_opy_ = True
            return
        bstack1ll1l1l11ll_opy_ = f.bstack1ll1l1ll111_opy_(*args)
        bstack1ll11ll1lll_opy_ = f.bstack1ll11ll11l1_opy_(*args)
        if bstack1ll1l1l11ll_opy_ and bstack1ll1l1l11ll_opy_.lower() == bstack1ll1l1_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦᅿ") and bstack1ll11ll1lll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11ll1lll_opy_.get(bstack1ll1l1_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᆀ"), None), bstack1ll11ll1lll_opy_.get(bstack1ll1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᆁ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢᆂ") + str(locator_value) + bstack1ll1l1_opy_ (u"ࠥࠦᆃ"))
                return
            def bstack11111ll111_opy_(driver, bstack1ll11ll1l11_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11ll1l11_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11ll1l1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1ll1l1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᆄ") + str(locator_value) + bstack1ll1l1_opy_ (u"ࠧࠨᆅ"))
                    else:
                        self.logger.warning(bstack1ll1l1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᆆ") + str(response) + bstack1ll1l1_opy_ (u"ࠢࠣᆇ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11ll1ll1_opy_(
                        driver, bstack1ll11ll1l11_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack11111ll111_opy_.__name__ = bstack1ll1l1l11ll_opy_
            return bstack11111ll111_opy_
    def __1ll11ll1ll1_opy_(
        self,
        driver,
        bstack1ll11ll1l11_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11ll1l1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1ll1l1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᆈ") + str(locator_value) + bstack1ll1l1_opy_ (u"ࠤࠥᆉ"))
                bstack1ll11lll1ll_opy_ = self.bstack1ll11ll11ll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1ll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥᆊ") + str(bstack1ll11lll1ll_opy_) + bstack1ll1l1_opy_ (u"ࠦࠧᆋ"))
                if bstack1ll11lll1ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1ll1l1_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᆌ"): bstack1ll11lll1ll_opy_.locator_type,
                            bstack1ll1l1_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᆍ"): bstack1ll11lll1ll_opy_.locator_value,
                        }
                    )
                    return bstack1ll11ll1l11_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1ll1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣᆎ"), False):
                    self.logger.info(bstack1lllll1ll11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨᆏ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1ll1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᆐ") + str(response) + bstack1ll1l1_opy_ (u"ࠥࠦᆑ"))
        except Exception as err:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣᆒ") + str(err) + bstack1ll1l1_opy_ (u"ࠧࠨᆓ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11lll1l1_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1ll11ll1l1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1ll1l1_opy_ (u"ࠨ࠰ࠣᆔ"),
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1ll1l1_opy_ (u"ࠢࠣᆕ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llllll1ll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1ll1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᆖ") + str(r) + bstack1ll1l1_opy_ (u"ࠤࠥᆗ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᆘ") + str(e) + bstack1ll1l1_opy_ (u"ࠦࠧᆙ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11llll11_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1ll11ll11ll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1ll1l1_opy_ (u"ࠧ࠶ࠢᆚ")):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llllll1ll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1ll1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆛ") + str(r) + bstack1ll1l1_opy_ (u"ࠢࠣᆜ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆝ") + str(e) + bstack1ll1l1_opy_ (u"ࠤࠥᆞ"))
            traceback.print_exc()
            raise e