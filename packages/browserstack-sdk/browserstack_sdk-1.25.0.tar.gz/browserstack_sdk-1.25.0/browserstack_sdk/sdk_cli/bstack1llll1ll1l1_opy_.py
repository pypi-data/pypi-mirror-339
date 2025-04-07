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
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111l11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll111lll_opy_(bstack1lllll1l111_opy_):
    bstack1ll1ll1l11l_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.PRE), self.bstack1ll11lll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11lll11l_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11lll1ll_opy_(hub_url):
            if not bstack1llll111lll_opy_.bstack1ll1ll1l11l_opy_:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠤ࡯ࡳࡨࡧ࡬ࠡࡵࡨࡰ࡫࠳ࡨࡦࡣ࡯ࠤ࡫ࡲ࡯ࡸࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡪࡰࡩࡶࡦࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᅻ") + str(hub_url) + bstack11l1l11_opy_ (u"ࠥࠦᅼ"))
                bstack1llll111lll_opy_.bstack1ll1ll1l11l_opy_ = True
            return
        bstack1ll1l1ll111_opy_ = f.bstack1ll1ll1l111_opy_(*args)
        bstack1ll1l11111l_opy_ = f.bstack1ll11lll1l1_opy_(*args)
        if bstack1ll1l1ll111_opy_ and bstack1ll1l1ll111_opy_.lower() == bstack11l1l11_opy_ (u"ࠦ࡫࡯࡮ࡥࡧ࡯ࡩࡲ࡫࡮ࡵࠤᅽ") and bstack1ll1l11111l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1l11111l_opy_.get(bstack11l1l11_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᅾ"), None), bstack1ll1l11111l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᅿ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡼࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࡽ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡺࡹࡩ࡯ࡩࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡼࡡ࡭ࡷࡨࡁࠧᆀ") + str(locator_value) + bstack11l1l11_opy_ (u"ࠣࠤᆁ"))
                return
            def bstack1111l1l111_opy_(driver, bstack1ll1l111111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1l111111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11llll11_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11l1l11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᆂ") + str(locator_value) + bstack11l1l11_opy_ (u"ࠥࠦᆃ"))
                    else:
                        self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᆄ") + str(response) + bstack11l1l11_opy_ (u"ࠧࠨᆅ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11lll111_opy_(
                        driver, bstack1ll1l111111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1111l1l111_opy_.__name__ = bstack1ll1l1ll111_opy_
            return bstack1111l1l111_opy_
    def __1ll11lll111_opy_(
        self,
        driver,
        bstack1ll1l111111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11llll11_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡶࡵ࡭࡬࡭ࡥࡳࡧࡧ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᆆ") + str(locator_value) + bstack11l1l11_opy_ (u"ࠢࠣᆇ"))
                bstack1ll11llll1l_opy_ = self.bstack1ll11llllll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡨࡦࡣ࡯࡭ࡳ࡭࡟ࡳࡧࡶࡹࡱࡺ࠽ࠣᆈ") + str(bstack1ll11llll1l_opy_) + bstack11l1l11_opy_ (u"ࠤࠥᆉ"))
                if bstack1ll11llll1l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11l1l11_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᆊ"): bstack1ll11llll1l_opy_.locator_type,
                            bstack11l1l11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᆋ"): bstack1ll11llll1l_opy_.locator_value,
                        }
                    )
                    return bstack1ll1l111111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡏ࡟ࡅࡇࡅ࡙ࡌࠨᆌ"), False):
                    self.logger.info(bstack1lll1l111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠮࡯࡬ࡷࡸ࡯࡮ࡨ࠼ࠣࡷࡱ࡫ࡥࡱࠪ࠶࠴࠮ࠦ࡬ࡦࡶࡷ࡭ࡳ࡭ࠠࡺࡱࡸࠤ࡮ࡴࡳࡱࡧࡦࡸࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠦ࡬ࡰࡩࡶࠦᆍ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᆎ") + str(response) + bstack11l1l11_opy_ (u"ࠣࠤᆏ"))
        except Exception as err:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨᆐ") + str(err) + bstack11l1l11_opy_ (u"ࠥࠦᆑ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11ll1lll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1ll11llll11_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11l1l11_opy_ (u"ࠦ࠵ࠨᆒ"),
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11l1l11_opy_ (u"ࠧࠨᆓ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll11lll1l_opy_.AISelfHealStep(req)
            self.logger.info(bstack11l1l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆔ") + str(r) + bstack11l1l11_opy_ (u"ࠢࠣᆕ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆖ") + str(e) + bstack11l1l11_opy_ (u"ࠤࠥᆗ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11lllll1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1ll11llllll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11l1l11_opy_ (u"ࠥ࠴ࠧᆘ")):
        self.bstack1ll1l1111l1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll11lll1l_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11l1l11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᆙ") + str(r) + bstack11l1l11_opy_ (u"ࠧࠨᆚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆛ") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣᆜ"))
            traceback.print_exc()
            raise e