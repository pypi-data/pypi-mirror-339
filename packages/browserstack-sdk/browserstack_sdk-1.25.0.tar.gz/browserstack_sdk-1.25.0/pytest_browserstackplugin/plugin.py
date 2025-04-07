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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l1ll1l11l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll111ll1_opy_, bstack1l1lll11l_opy_, update, bstack1l11111l11_opy_,
                                       bstack111lllll_opy_, bstack1ll111l11_opy_, bstack11ll1ll1_opy_, bstack1ll1llll1l_opy_,
                                       bstack1l11l1l1_opy_, bstack11l11ll1ll_opy_, bstack11lll1ll1l_opy_, bstack1lll11ll11_opy_,
                                       bstack1l11l1ll1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111111_opy_)
from browserstack_sdk.bstack11l1llll11_opy_ import bstack11ll111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack111ll1l11_opy_
from bstack_utils.capture import bstack11l11111ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11lll1l1l_opy_, bstack11lllll11_opy_, bstack1111lll11_opy_, \
    bstack1111111ll_opy_
from bstack_utils.helper import bstack1llllllll1_opy_, bstack11ll1l111ll_opy_, bstack111l1l1l11_opy_, bstack1lll1l1ll1_opy_, bstack1ll1111l1ll_opy_, bstack1ll11ll11_opy_, \
    bstack11ll11l1l11_opy_, \
    bstack11lll1l1l11_opy_, bstack1ll1lllll_opy_, bstack11111l1l_opy_, bstack11ll1ll1111_opy_, bstack1lll1ll11l_opy_, Notset, \
    bstack11l1l1l11l_opy_, bstack11ll1ll1ll1_opy_, bstack11ll1l111l1_opy_, Result, bstack11ll1ll11l1_opy_, bstack11ll11l11l1_opy_, bstack111ll1l1l1_opy_, \
    bstack1l11llll_opy_, bstack1l111lll1_opy_, bstack1ll11l1l1_opy_, bstack11lll1l11ll_opy_
from bstack_utils.bstack11l1lll1l11_opy_ import bstack11l1ll1ll1l_opy_
from bstack_utils.messages import bstack11ll1l1111_opy_, bstack1111llll_opy_, bstack11l1ll1ll_opy_, bstack1l11ll11ll_opy_, bstack1ll11lllll_opy_, \
    bstack111l1llll_opy_, bstack1lll1l1ll_opy_, bstack111l11l1_opy_, bstack11l1ll111l_opy_, bstack111111ll_opy_, \
    bstack1l11l1111l_opy_, bstack11l1l1ll1l_opy_
from bstack_utils.proxy import bstack11ll1l1l1_opy_, bstack11llll1l_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111lll1ll11_opy_, bstack111lll1l111_opy_, bstack111lll111ll_opy_, bstack111lll11lll_opy_, \
    bstack111lll1l1ll_opy_, bstack111lll11l11_opy_, bstack111lll1l11l_opy_, bstack111l1l1l1_opy_, bstack111lll11l1l_opy_
from bstack_utils.bstack1l11llll1_opy_ import bstack1ll111l1l_opy_
from bstack_utils.bstack11lll1l1_opy_ import bstack11ll11111_opy_, bstack1l1ll1ll_opy_, bstack1ll11l1l1l_opy_, \
    bstack1l1l1l11l1_opy_, bstack1llll1lll1_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack11l1111111_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack11l11l11_opy_
import bstack_utils.accessibility as bstack1l1l1l1ll1_opy_
from bstack_utils.bstack11l111l1l1_opy_ import bstack11lll111l1_opy_
from bstack_utils.bstack11ll1lll1l_opy_ import bstack11ll1lll1l_opy_
from browserstack_sdk.__init__ import bstack1lll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack11l11ll11l_opy_ import bstack11l11ll11l_opy_, bstack1llll111ll_opy_, bstack111111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11lll1l11_opy_, bstack1llllll1lll_opy_, bstack1lll111lll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l11ll11l_opy_ import bstack11l11ll11l_opy_, bstack1llll111ll_opy_, bstack111111ll1_opy_
bstack1lll1l1l_opy_ = None
bstack1lllll11l1_opy_ = None
bstack1l1llll11_opy_ = None
bstack1lll11l1ll_opy_ = None
bstack1ll111ll_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1ll111l1_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1l1l1lll_opy_ = None
bstack1l1111111l_opy_ = None
bstack11llll11ll_opy_ = None
bstack1l1111ll1l_opy_ = None
bstack11ll11lll_opy_ = None
bstack1l11lll1l_opy_ = bstack11l1l11_opy_ (u"ࠧࠨẵ")
CONFIG = {}
bstack11ll11l11l_opy_ = False
bstack1111l1l1_opy_ = bstack11l1l11_opy_ (u"ࠨࠩẶ")
bstack11l1ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠩࠪặ")
bstack111lll11_opy_ = False
bstack1l11ll11l1_opy_ = []
bstack1llll1ll1l_opy_ = bstack11lll1l1l_opy_
bstack1111lll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪẸ")
bstack1l11lll1ll_opy_ = {}
bstack11l1l1lll_opy_ = None
bstack1l1l1lll1l_opy_ = False
logger = bstack111ll1l11_opy_.get_logger(__name__, bstack1llll1ll1l_opy_)
store = {
    bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨẹ"): []
}
bstack1111lll11l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111ll1l1ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11lll1l11_opy_(
    test_framework_name=bstack1l1111l1l1_opy_[bstack11l1l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩẺ")] if bstack1lll1ll11l_opy_() else bstack1l1111l1l1_opy_[bstack11l1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭ẻ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l11ll1l11_opy_(page, bstack1l111lll_opy_):
    try:
        page.evaluate(bstack11l1l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣẼ"),
                      bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬẽ") + json.dumps(
                          bstack1l111lll_opy_) + bstack11l1l11_opy_ (u"ࠤࢀࢁࠧẾ"))
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣế"), e)
def bstack1lll111l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1l11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧỀ"), bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪề") + json.dumps(
            message) + bstack11l1l11_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩỂ") + json.dumps(level) + bstack11l1l11_opy_ (u"ࠧࡾࡿࠪể"))
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦỄ"), e)
def pytest_configure(config):
    global bstack1111l1l1_opy_
    global CONFIG
    bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
    config.args = bstack11l11l11_opy_.bstack111l111ll11_opy_(config.args)
    bstack111ll1lll_opy_.bstack11l11l11l_opy_(bstack1ll11l1l1_opy_(config.getoption(bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ễ"))))
    try:
        bstack111ll1l11_opy_.bstack11l1l1lll11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.CONNECT, bstack111111ll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪỆ"), bstack11l1l11_opy_ (u"ࠫ࠵࠭ệ")))
        config = json.loads(os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦỈ"), bstack11l1l11_opy_ (u"ࠨࡻࡾࠤỉ")))
        cli.bstack1llll11l111_opy_(bstack11111l1l_opy_(bstack1111l1l1_opy_, CONFIG), cli_context.platform_index, bstack1l11111l11_opy_)
    if cli.bstack1lll111111l_opy_(bstack1lll1ll1111_opy_):
        cli.bstack1lll1lllll1_opy_()
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨỊ") + str(cli_context.platform_index) + bstack11l1l11_opy_ (u"ࠣࠤị"))
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.BEFORE_ALL, bstack1lll111lll1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11l1l11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢỌ"), None)
    if cli.is_running() and when == bstack11l1l11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣọ"):
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.LOG_REPORT, bstack1lll111lll1_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥỎ"):
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.BEFORE_EACH, bstack1lll111lll1_opy_.POST, item, call, outcome)
        elif when == bstack11l1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥỏ"):
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.LOG_REPORT, bstack1lll111lll1_opy_.POST, item, call, outcome)
        elif when == bstack11l1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣỐ"):
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.AFTER_EACH, bstack1lll111lll1_opy_.POST, item, call, outcome)
        return # skip all existing bstack111l111l11l_opy_
    bstack111l1111l1l_opy_ = item.config.getoption(bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩố"))
    plugins = item.config.getoption(bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤỒ"))
    report = outcome.get_result()
    bstack111l1111lll_opy_(item, call, report)
    if bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢồ") not in plugins or bstack1lll1ll11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1l11_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦỔ"), None)
    page = getattr(item, bstack11l1l11_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥổ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1111llllll1_opy_(item, report, summary, bstack111l1111l1l_opy_)
    if (page is not None):
        bstack111l11111l1_opy_(item, report, summary, bstack111l1111l1l_opy_)
def bstack1111llllll1_opy_(item, report, summary, bstack111l1111l1l_opy_):
    if report.when == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫỖ") and report.skipped:
        bstack111lll11l1l_opy_(report)
    if report.when in [bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧỗ"), bstack11l1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤỘ")]:
        return
    if not bstack1ll1111l1ll_opy_():
        return
    try:
        if (str(bstack111l1111l1l_opy_).lower() != bstack11l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ộ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧỚ") + json.dumps(
                    report.nodeid) + bstack11l1l11_opy_ (u"ࠪࢁࢂ࠭ớ"))
        os.environ[bstack11l1l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧỜ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧờ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣỞ")))
    bstack1ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠢࠣở")
    bstack111lll11l1l_opy_(report)
    if not passed:
        try:
            bstack1ll11l1111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣỠ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11l1111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦỡ")))
        bstack1ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠥࠦỢ")
        if not passed:
            try:
                bstack1ll11l1111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦợ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11l1111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩỤ")
                    + json.dumps(bstack11l1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢụ"))
                    + bstack11l1l11_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥỦ")
                )
            else:
                item._driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ủ")
                    + json.dumps(str(bstack1ll11l1111_opy_))
                    + bstack11l1l11_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧỨ")
                )
        except Exception as e:
            summary.append(bstack11l1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣứ").format(e))
def bstack1111llll1l1_opy_(test_name, error_message):
    try:
        bstack1111llll11l_opy_ = []
        bstack1l1l1l111_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫỪ"), bstack11l1l11_opy_ (u"ࠬ࠶ࠧừ"))
        bstack11ll111ll1_opy_ = {bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫỬ"): test_name, bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ử"): error_message, bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧỮ"): bstack1l1l1l111_opy_}
        bstack1111lll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧữ"))
        if os.path.exists(bstack1111lll1l1l_opy_):
            with open(bstack1111lll1l1l_opy_) as f:
                bstack1111llll11l_opy_ = json.load(f)
        bstack1111llll11l_opy_.append(bstack11ll111ll1_opy_)
        with open(bstack1111lll1l1l_opy_, bstack11l1l11_opy_ (u"ࠪࡻࠬỰ")) as f:
            json.dump(bstack1111llll11l_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩự") + str(e))
def bstack111l11111l1_opy_(item, report, summary, bstack111l1111l1l_opy_):
    if report.when in [bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦỲ"), bstack11l1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣỳ")]:
        return
    if (str(bstack111l1111l1l_opy_).lower() != bstack11l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬỴ")):
        bstack1l11ll1l11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥỵ")))
    bstack1ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠤࠥỶ")
    bstack111lll11l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll11l1111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥỷ").format(e)
                )
        try:
            if passed:
                bstack1llll1lll1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪỸ"), None), bstack11l1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧỹ"))
            else:
                error_message = bstack11l1l11_opy_ (u"࠭ࠧỺ")
                if bstack1ll11l1111_opy_:
                    bstack1lll111l1l_opy_(item._page, str(bstack1ll11l1111_opy_), bstack11l1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨỻ"))
                    bstack1llll1lll1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧỼ"), None), bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤỽ"), str(bstack1ll11l1111_opy_))
                    error_message = str(bstack1ll11l1111_opy_)
                else:
                    bstack1llll1lll1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩỾ"), None), bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦỿ"))
                bstack1111llll1l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤἀ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11l1l11_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥἁ"), default=bstack11l1l11_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨἂ"), help=bstack11l1l11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢἃ"))
    parser.addoption(bstack11l1l11_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣἄ"), default=bstack11l1l11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤἅ"), help=bstack11l1l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥἆ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1l11_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢἇ"), action=bstack11l1l11_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧἈ"), default=bstack11l1l11_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢἉ"),
                         help=bstack11l1l11_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢἊ"))
def bstack11l1111l1l_opy_(log):
    if not (log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪἋ")] and log[bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫἌ")].strip()):
        return
    active = bstack11l111lll1_opy_()
    log = {
        bstack11l1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪἍ"): log[bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫἎ")],
        bstack11l1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩἏ"): bstack111l1l1l11_opy_().isoformat() + bstack11l1l11_opy_ (u"࡛ࠧࠩἐ"),
        bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩἑ"): log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪἒ")],
    }
    if active:
        if active[bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨἓ")] == bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩἔ"):
            log[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬἕ")] = active[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭἖")]
        elif active[bstack11l1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ἗")] == bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭Ἐ"):
            log[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩἙ")] = active[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪἚ")]
    bstack11lll111l1_opy_.bstack1lll1l1111_opy_([log])
def bstack11l111lll1_opy_():
    if len(store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨἛ")]) > 0 and store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩἜ")][-1]:
        return {
            bstack11l1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫἝ"): bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ἞"),
            bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ἟"): store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ἠ")][-1]
        }
    if store.get(bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧἡ"), None):
        return {
            bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩἢ"): bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࠪἣ"),
            bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ἤ"): store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫἥ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.INIT_TEST, bstack1lll111lll1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.INIT_TEST, bstack1lll111lll1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._111l111111l_opy_ = True
        bstack11l11llll1_opy_ = bstack1l1l1l1ll1_opy_.bstack11lll111_opy_(bstack11lll1l1l11_opy_(item.own_markers))
        if not cli.bstack1lll111111l_opy_(bstack1lll1ll1111_opy_):
            item._a11y_test_case = bstack11l11llll1_opy_
            if bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧἦ"), None):
                driver = getattr(item, bstack11l1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪἧ"), None)
                item._a11y_started = bstack1l1l1l1ll1_opy_.bstack1l111l11l1_opy_(driver, bstack11l11llll1_opy_)
        if not bstack11lll111l1_opy_.on() or bstack1111lll1ll1_opy_ != bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪἨ"):
            return
        global current_test_uuid #, bstack11l1111l11_opy_
        bstack111l11lll1_opy_ = {
            bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩἩ"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩἪ"): bstack111l1l1l11_opy_().isoformat() + bstack11l1l11_opy_ (u"࡚࠭ࠨἫ")
        }
        current_test_uuid = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬἬ")]
        store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬἭ")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧἮ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111ll1l1ll_opy_[item.nodeid] = {**_111ll1l1ll_opy_[item.nodeid], **bstack111l11lll1_opy_}
        bstack111l1111ll1_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫἯ"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ἰ"), str(err))
def pytest_runtest_setup(item):
    store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩἱ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.BEFORE_EACH, bstack1lll111lll1_opy_.PRE, item, bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬἲ"))
        return # skip all existing bstack111l111l11l_opy_
    global bstack1111lll11l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll1ll1111_opy_():
        atexit.register(bstack1l111ll1l_opy_)
        if not bstack1111lll11l1_opy_:
            try:
                bstack1111lllll1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11lll1l11ll_opy_():
                    bstack1111lllll1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1111lllll1l_opy_:
                    signal.signal(s, bstack1111lll1111_opy_)
                bstack1111lll11l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣἳ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111lll1ll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨἴ")
    try:
        if not bstack11lll111l1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11lll1_opy_ = {
            bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧἵ"): uuid,
            bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἶ"): bstack111l1l1l11_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠫ࡟࠭ἷ"),
            bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪἸ"): bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫἹ"),
            bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪἺ"): bstack11l1l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ἳ"),
            bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬἼ"): bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩἽ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨἾ")] = item
        store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩἿ")] = [uuid]
        if not _111ll1l1ll_opy_.get(item.nodeid, None):
            _111ll1l1ll_opy_[item.nodeid] = {bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬὀ"): [], bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩὁ"): []}
        _111ll1l1ll_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧὂ")].append(bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧὃ")])
        _111ll1l1ll_opy_[item.nodeid + bstack11l1l11_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪὄ")] = bstack111l11lll1_opy_
        bstack111l111l111_opy_(item, bstack111l11lll1_opy_, bstack11l1l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬὅ"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ὆"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.AFTER_EACH, bstack1lll111lll1_opy_.PRE, item, bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ὇"))
        return # skip all existing bstack111l111l11l_opy_
    try:
        global bstack1l11lll1ll_opy_
        bstack1l1l1l111_opy_ = 0
        if bstack111lll11_opy_ is True:
            bstack1l1l1l111_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧὈ")))
        if bstack111l11l1l_opy_.bstack1ll1111111_opy_() == bstack11l1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨὉ"):
            if bstack111l11l1l_opy_.bstack11lllll1_opy_() == bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦὊ"):
                bstack1111lll1l11_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ὃ"), None)
                bstack1l1l1llll1_opy_ = bstack1111lll1l11_opy_ + bstack11l1l11_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢὌ")
                driver = getattr(item, bstack11l1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭Ὅ"), None)
                bstack1ll11l111l_opy_ = getattr(item, bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ὎"), None)
                bstack1ll111l1ll_opy_ = getattr(item, bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ὏"), None)
                PercySDK.screenshot(driver, bstack1l1l1llll1_opy_, bstack1ll11l111l_opy_=bstack1ll11l111l_opy_, bstack1ll111l1ll_opy_=bstack1ll111l1ll_opy_, bstack11l11111l_opy_=bstack1l1l1l111_opy_)
        if not cli.bstack1lll111111l_opy_(bstack1lll1ll1111_opy_):
            if getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨὐ"), False):
                bstack11ll111l_opy_.bstack1lllllll1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪὑ"), None), bstack1l11lll1ll_opy_, logger, item)
        if not bstack11lll111l1_opy_.on():
            return
        bstack111l11lll1_opy_ = {
            bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨὒ"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨὓ"): bstack111l1l1l11_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠬࡠࠧὔ"),
            bstack11l1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫὕ"): bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬὖ"),
            bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫὗ"): bstack11l1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭὘"),
            bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭Ὑ"): bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭὚")
        }
        _111ll1l1ll_opy_[item.nodeid + bstack11l1l11_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨὛ")] = bstack111l11lll1_opy_
        bstack111l111l111_opy_(item, bstack111l11lll1_opy_, bstack11l1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ὜"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭Ὕ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111lll11lll_opy_(fixturedef.argname):
        store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ὞")] = request.node
    elif bstack111lll1l1ll_opy_(fixturedef.argname):
        store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧὟ")] = request.node
    if not bstack11lll111l1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.SETUP_FIXTURE, bstack1lll111lll1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.SETUP_FIXTURE, bstack1lll111lll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111l111l11l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.SETUP_FIXTURE, bstack1lll111lll1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.SETUP_FIXTURE, bstack1lll111lll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111l111l11l_opy_
    try:
        fixture = {
            bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨὠ"): fixturedef.argname,
            bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫὡ"): bstack11ll11l1l11_opy_(outcome),
            bstack11l1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧὢ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪὣ")]
        if not _111ll1l1ll_opy_.get(current_test_item.nodeid, None):
            _111ll1l1ll_opy_[current_test_item.nodeid] = {bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩὤ"): []}
        _111ll1l1ll_opy_[current_test_item.nodeid][bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪὥ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬὦ"), str(err))
if bstack1lll1ll11l_opy_() and bstack11lll111l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.STEP, bstack1lll111lll1_opy_.PRE, request, step)
            return
        try:
            _111ll1l1ll_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ὧ")].bstack1l1lll11l1_opy_(id(step))
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩὨ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.STEP, bstack1lll111lll1_opy_.POST, request, step, exception)
            return
        try:
            _111ll1l1ll_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨὩ")].bstack11l11l1l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪὪ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.STEP, bstack1lll111lll1_opy_.POST, request, step)
            return
        try:
            bstack111lllll1l_opy_: bstack11l1111111_opy_ = _111ll1l1ll_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪὫ")]
            bstack111lllll1l_opy_.bstack11l11l1l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬὬ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1111lll1ll1_opy_
        try:
            if not bstack11lll111l1_opy_.on() or bstack1111lll1ll1_opy_ != bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭Ὥ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.TEST, bstack1lll111lll1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩὮ"), None)
            if not _111ll1l1ll_opy_.get(request.node.nodeid, None):
                _111ll1l1ll_opy_[request.node.nodeid] = {}
            bstack111lllll1l_opy_ = bstack11l1111111_opy_.bstack111l1llll1l_opy_(
                scenario, feature, request.node,
                name=bstack111lll11l11_opy_(request.node, scenario),
                started_at=bstack1ll11ll11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭Ὧ"),
                tags=bstack111lll1l11l_opy_(feature, scenario),
                bstack11l111l11l_opy_=bstack11lll111l1_opy_.bstack11l11l111l_opy_(driver) if driver and driver.session_id else {}
            )
            _111ll1l1ll_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨὰ")] = bstack111lllll1l_opy_
            bstack111l1111111_opy_(bstack111lllll1l_opy_.uuid)
            bstack11lll111l1_opy_.bstack111lllllll_opy_(bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧά"), bstack111lllll1l_opy_)
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩὲ"), str(err))
def bstack1111llll111_opy_(bstack11l11l11l1_opy_):
    if bstack11l11l11l1_opy_ in store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬέ")]:
        store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ὴ")].remove(bstack11l11l11l1_opy_)
def bstack111l1111111_opy_(test_uuid):
    store[bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧή")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack11lll111l1_opy_.bstack111l1l11111_opy_
def bstack111l1111lll_opy_(item, call, report):
    logger.debug(bstack11l1l11_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡶࡹ࠭ὶ"))
    global bstack1111lll1ll1_opy_
    bstack1111l111l_opy_ = bstack1ll11ll11_opy_()
    if hasattr(report, bstack11l1l11_opy_ (u"ࠬࡹࡴࡰࡲࠪί")):
        bstack1111l111l_opy_ = bstack11ll1ll11l1_opy_(report.stop)
    elif hasattr(report, bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬὸ")):
        bstack1111l111l_opy_ = bstack11ll1ll11l1_opy_(report.start)
    try:
        if getattr(report, bstack11l1l11_opy_ (u"ࠧࡸࡪࡨࡲࠬό"), bstack11l1l11_opy_ (u"ࠨࠩὺ")) == bstack11l1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧύ"):
            logger.debug(bstack11l1l11_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬὼ").format(getattr(report, bstack11l1l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩώ"), bstack11l1l11_opy_ (u"ࠬ࠭὾")).__str__(), bstack1111lll1ll1_opy_))
            if bstack1111lll1ll1_opy_ == bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭὿"):
                _111ll1l1ll_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᾀ")] = bstack1111l111l_opy_
                bstack111l1111ll1_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᾁ"), report, call)
                store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᾂ")] = None
            elif bstack1111lll1ll1_opy_ == bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᾃ"):
                bstack111lllll1l_opy_ = _111ll1l1ll_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᾄ")]
                bstack111lllll1l_opy_.set(hooks=_111ll1l1ll_opy_[item.nodeid].get(bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᾅ"), []))
                exception, bstack11l11l1l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l11l1l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l1l11_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬᾆ"), bstack11l1l11_opy_ (u"ࠧࠨᾇ"))]
                bstack111lllll1l_opy_.stop(time=bstack1111l111l_opy_, result=Result(result=getattr(report, bstack11l1l11_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᾈ"), bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᾉ")), exception=exception, bstack11l11l1l11_opy_=bstack11l11l1l11_opy_))
                bstack11lll111l1_opy_.bstack111lllllll_opy_(bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᾊ"), _111ll1l1ll_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᾋ")])
        elif getattr(report, bstack11l1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᾌ"), bstack11l1l11_opy_ (u"࠭ࠧᾍ")) in [bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᾎ"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᾏ")]:
            logger.debug(bstack11l1l11_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫᾐ").format(getattr(report, bstack11l1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᾑ"), bstack11l1l11_opy_ (u"ࠫࠬᾒ")).__str__(), bstack1111lll1ll1_opy_))
            bstack11l111l111_opy_ = item.nodeid + bstack11l1l11_opy_ (u"ࠬ࠳ࠧᾓ") + getattr(report, bstack11l1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫᾔ"), bstack11l1l11_opy_ (u"ࠧࠨᾕ"))
            if getattr(report, bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᾖ"), False):
                hook_type = bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᾗ") if getattr(report, bstack11l1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᾘ"), bstack11l1l11_opy_ (u"ࠫࠬᾙ")) == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᾚ") else bstack11l1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᾛ")
                _111ll1l1ll_opy_[bstack11l111l111_opy_] = {
                    bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᾜ"): uuid4().__str__(),
                    bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᾝ"): bstack1111l111l_opy_,
                    bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᾞ"): hook_type
                }
            _111ll1l1ll_opy_[bstack11l111l111_opy_][bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᾟ")] = bstack1111l111l_opy_
            bstack1111llll111_opy_(_111ll1l1ll_opy_[bstack11l111l111_opy_][bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᾠ")])
            bstack111l111l111_opy_(item, _111ll1l1ll_opy_[bstack11l111l111_opy_], bstack11l1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᾡ"), report, call)
            if getattr(report, bstack11l1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫᾢ"), bstack11l1l11_opy_ (u"ࠧࠨᾣ")) == bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᾤ"):
                if getattr(report, bstack11l1l11_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᾥ"), bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᾦ")) == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᾧ"):
                    bstack111l11lll1_opy_ = {
                        bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᾨ"): uuid4().__str__(),
                        bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᾩ"): bstack1ll11ll11_opy_(),
                        bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᾪ"): bstack1ll11ll11_opy_()
                    }
                    _111ll1l1ll_opy_[item.nodeid] = {**_111ll1l1ll_opy_[item.nodeid], **bstack111l11lll1_opy_}
                    bstack111l1111ll1_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᾫ"))
                    bstack111l1111ll1_opy_(item, _111ll1l1ll_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᾬ"), report, call)
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᾭ"), str(err))
def bstack1111lllllll_opy_(test, bstack111l11lll1_opy_, result=None, call=None, bstack1ll1ll1ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lllll1l_opy_ = {
        bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᾮ"): bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᾯ")],
        bstack11l1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᾰ"): bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࠬᾱ"),
        bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᾲ"): test.name,
        bstack11l1l11_opy_ (u"ࠩࡥࡳࡩࡿࠧᾳ"): {
            bstack11l1l11_opy_ (u"ࠪࡰࡦࡴࡧࠨᾴ"): bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᾵"),
            bstack11l1l11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᾶ"): inspect.getsource(test.obj)
        },
        bstack11l1l11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᾷ"): test.name,
        bstack11l1l11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭Ᾰ"): test.name,
        bstack11l1l11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᾹ"): bstack11l11l11_opy_.bstack111l1l111l_opy_(test),
        bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᾺ"): file_path,
        bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬΆ"): file_path,
        bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᾼ"): bstack11l1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭᾽"),
        bstack11l1l11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫι"): file_path,
        bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᾿"): bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ῀")],
        bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ῁"): bstack11l1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪῂ"),
        bstack11l1l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧῃ"): {
            bstack11l1l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩῄ"): test.nodeid
        },
        bstack11l1l11_opy_ (u"࠭ࡴࡢࡩࡶࠫ῅"): bstack11lll1l1l11_opy_(test.own_markers)
    }
    if bstack1ll1ll1ll_opy_ in [bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨῆ"), bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪῇ")]:
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠩࡰࡩࡹࡧࠧῈ")] = {
            bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬΈ"): bstack111l11lll1_opy_.get(bstack11l1l11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭Ὴ"), [])
        }
    if bstack1ll1ll1ll_opy_ == bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭Ή"):
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ῌ")] = bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ῍")
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ῎")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ῏")]
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨῐ")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩῑ")]
    if result:
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬῒ")] = result.outcome
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧΐ")] = result.duration * 1000
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ῔")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭῕")]
        if result.failed:
            bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨῖ")] = bstack11lll111l1_opy_.bstack1111ll1lll_opy_(call.excinfo.typename)
            bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫῗ")] = bstack11lll111l1_opy_.bstack111l11lll11_opy_(call.excinfo, result)
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪῘ")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫῙ")]
    if outcome:
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Ὶ")] = bstack11ll11l1l11_opy_(outcome)
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨΊ")] = 0
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭῜")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ῝")]
        if bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ῞")] == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ῟"):
            bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫῠ")] = bstack11l1l11_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧῡ")  # bstack1111lllll11_opy_
            bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨῢ")] = [{bstack11l1l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫΰ"): [bstack11l1l11_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ῤ")]}]
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩῥ")] = bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪῦ")]
    return bstack111lllll1l_opy_
def bstack1111lll11ll_opy_(test, bstack111l1l1lll_opy_, bstack1ll1ll1ll_opy_, result, call, outcome, bstack1111ll1ll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨῧ")]
    hook_name = bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩῨ")]
    hook_data = {
        bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬῩ"): bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ὺ")],
        bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧΎ"): bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨῬ"),
        bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ῭"): bstack11l1l11_opy_ (u"ࠬࢁࡽࠨ΅").format(bstack111lll1l111_opy_(hook_name)),
        bstack11l1l11_opy_ (u"࠭ࡢࡰࡦࡼࠫ`"): {
            bstack11l1l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ῰"): bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ῱"),
            bstack11l1l11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧῲ"): None
        },
        bstack11l1l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩῳ"): test.name,
        bstack11l1l11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫῴ"): bstack11l11l11_opy_.bstack111l1l111l_opy_(test, hook_name),
        bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ῵"): file_path,
        bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨῶ"): file_path,
        bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧῷ"): bstack11l1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩῸ"),
        bstack11l1l11_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧΌ"): file_path,
        bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧῺ"): bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨΏ")],
        bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨῼ"): bstack11l1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ´") if bstack1111lll1ll1_opy_ == bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ῾") else bstack11l1l11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ῿"),
        bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ "): hook_type
    }
    bstack111l1lll1l1_opy_ = bstack111l11ll1l_opy_(_111ll1l1ll_opy_.get(test.nodeid, None))
    if bstack111l1lll1l1_opy_:
        hook_data[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ ")] = bstack111l1lll1l1_opy_
    if result:
        hook_data[bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ ")] = result.outcome
        hook_data[bstack11l1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ ")] = result.duration * 1000
        hook_data[bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ ")] = bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ ")]
        if result.failed:
            hook_data[bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ ")] = bstack11lll111l1_opy_.bstack1111ll1lll_opy_(call.excinfo.typename)
            hook_data[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ ")] = bstack11lll111l1_opy_.bstack111l11lll11_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ ")] = bstack11ll11l1l11_opy_(outcome)
        hook_data[bstack11l1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ ")] = 100
        hook_data[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ ")] = bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ​")]
        if hook_data[bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ‌")] == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ‍"):
            hook_data[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ‎")] = bstack11l1l11_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ‏")  # bstack1111lllll11_opy_
            hook_data[bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ‐")] = [{bstack11l1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ‑"): [bstack11l1l11_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ‒")]}]
    if bstack1111ll1ll1l_opy_:
        hook_data[bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ–")] = bstack1111ll1ll1l_opy_.result
        hook_data[bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ—")] = bstack11ll1ll1ll1_opy_(bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭―")], bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ‖")])
        hook_data[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ‗")] = bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ‘")]
        if hook_data[bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭’")] == bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ‚"):
            hook_data[bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ‛")] = bstack11lll111l1_opy_.bstack1111ll1lll_opy_(bstack1111ll1ll1l_opy_.exception_type)
            hook_data[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ“")] = [{bstack11l1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭”"): bstack11ll1l111l1_opy_(bstack1111ll1ll1l_opy_.exception)}]
    return hook_data
def bstack111l1111ll1_opy_(test, bstack111l11lll1_opy_, bstack1ll1ll1ll_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11l1l11_opy_ (u"ࠫࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ„").format(bstack1ll1ll1ll_opy_))
    bstack111lllll1l_opy_ = bstack1111lllllll_opy_(test, bstack111l11lll1_opy_, result, call, bstack1ll1ll1ll_opy_, outcome)
    driver = getattr(test, bstack11l1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭‟"), None)
    if bstack1ll1ll1ll_opy_ == bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ†") and driver:
        bstack111lllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭‡")] = bstack11lll111l1_opy_.bstack11l11l111l_opy_(driver)
    if bstack1ll1ll1ll_opy_ == bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ•"):
        bstack1ll1ll1ll_opy_ = bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ‣")
    bstack111ll11ll1_opy_ = {
        bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ․"): bstack1ll1ll1ll_opy_,
        bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭‥"): bstack111lllll1l_opy_
    }
    bstack11lll111l1_opy_.bstack1ll1l1l1ll_opy_(bstack111ll11ll1_opy_)
    if bstack1ll1ll1ll_opy_ == bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭…"):
        threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭‧"): bstack11l1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ ")}
    elif bstack1ll1ll1ll_opy_ == bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ "):
        threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ‪"): getattr(result, bstack11l1l11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ‫"), bstack11l1l11_opy_ (u"ࠫࠬ‬"))}
def bstack111l111l111_opy_(test, bstack111l11lll1_opy_, bstack1ll1ll1ll_opy_, result=None, call=None, outcome=None, bstack1111ll1ll1l_opy_=None):
    logger.debug(bstack11l1l11_opy_ (u"ࠬࡹࡥ࡯ࡦࡢ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡩࡱࡲ࡯ࠥࡪࡡࡵࡣ࠯ࠤࡪࡼࡥ࡯ࡶࡗࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ‭").format(bstack1ll1ll1ll_opy_))
    hook_data = bstack1111lll11ll_opy_(test, bstack111l11lll1_opy_, bstack1ll1ll1ll_opy_, result, call, outcome, bstack1111ll1ll1l_opy_)
    bstack111ll11ll1_opy_ = {
        bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ‮"): bstack1ll1ll1ll_opy_,
        bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ "): hook_data
    }
    bstack11lll111l1_opy_.bstack1ll1l1l1ll_opy_(bstack111ll11ll1_opy_)
def bstack111l11ll1l_opy_(bstack111l11lll1_opy_):
    if not bstack111l11lll1_opy_:
        return None
    if bstack111l11lll1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ‰"), None):
        return getattr(bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ‱")], bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ′"), None)
    return bstack111l11lll1_opy_.get(bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ″"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.LOG, bstack1lll111lll1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_.LOG, bstack1lll111lll1_opy_.POST, request, caplog)
        return # skip all existing bstack111l111l11l_opy_
    try:
        if not bstack11lll111l1_opy_.on():
            return
        places = [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ‴"), bstack11l1l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ‵"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ‶")]
        logs = []
        for bstack1111lll1lll_opy_ in places:
            records = caplog.get_records(bstack1111lll1lll_opy_)
            bstack1111ll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ‷") if bstack1111lll1lll_opy_ == bstack11l1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧ‸") else bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ‹")
            bstack1111llll1ll_opy_ = request.node.nodeid + (bstack11l1l11_opy_ (u"ࠫࠬ›") if bstack1111lll1lll_opy_ == bstack11l1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ※") else bstack11l1l11_opy_ (u"࠭࠭ࠨ‼") + bstack1111lll1lll_opy_)
            test_uuid = bstack111l11ll1l_opy_(_111ll1l1ll_opy_.get(bstack1111llll1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll11l11l1_opy_(record.message):
                    continue
                logs.append({
                    bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ‽"): bstack11ll1l111ll_opy_(record.created).isoformat() + bstack11l1l11_opy_ (u"ࠨ࡜ࠪ‾"),
                    bstack11l1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ‿"): record.levelname,
                    bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⁀"): record.message,
                    bstack1111ll1ll11_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack11lll111l1_opy_.bstack1lll1l1111_opy_(logs)
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ⁁"), str(err))
def bstack1ll11ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l1lll1l_opy_
    bstack1l11l1ll1_opy_ = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ⁂"), None) and bstack1llllllll1_opy_(
            threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⁃"), None)
    bstack1lll1111ll_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⁄"), None) != None and getattr(driver, bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⁅"), None) == True
    if sequence == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⁆") and driver != None:
      if not bstack1l1l1lll1l_opy_ and bstack1ll1111l1ll_opy_() and bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⁇") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁈")] == True and bstack11ll1lll1l_opy_.bstack11ll111111_opy_(driver_command) and (bstack1lll1111ll_opy_ or bstack1l11l1ll1_opy_) and not bstack1l111111_opy_(args):
        try:
          bstack1l1l1lll1l_opy_ = True
          logger.debug(bstack11l1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ⁉").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ⁊").format(str(err)))
        bstack1l1l1lll1l_opy_ = False
    if sequence == bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⁋"):
        if driver_command == bstack11l1l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ⁌"):
            bstack11lll111l1_opy_.bstack11ll1111ll_opy_({
                bstack11l1l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ⁍"): response[bstack11l1l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ⁎")],
                bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁏"): store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⁐")]
            })
def bstack1l111ll1l_opy_():
    global bstack1l11ll11l1_opy_
    bstack111ll1l11_opy_.bstack1l1l1111_opy_()
    logging.shutdown()
    bstack11lll111l1_opy_.bstack111l1l1ll1_opy_()
    for driver in bstack1l11ll11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111lll1111_opy_(*args):
    global bstack1l11ll11l1_opy_
    bstack11lll111l1_opy_.bstack111l1l1ll1_opy_()
    for driver in bstack1l11ll11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111ll111l_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1llll1ll_opy_(self, *args, **kwargs):
    bstack1llllll1l1_opy_ = bstack1lll1l1l_opy_(self, *args, **kwargs)
    bstack1ll11111l1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⁑"), None)
    if bstack1ll11111l1_opy_ and bstack1ll11111l1_opy_.get(bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⁒"), bstack11l1l11_opy_ (u"ࠨࠩ⁓")) == bstack11l1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⁔"):
        bstack11lll111l1_opy_.bstack11ll1111_opy_(self)
    return bstack1llllll1l1_opy_
@measure(event_name=EVENTS.bstack1l1l11l1l1_opy_, stage=STAGE.bstack1ll11l11ll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1l1111l11l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
    if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⁕")):
        return
    bstack111ll1lll_opy_.bstack11l111l1_opy_(bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⁖"), True)
    global bstack1l11lll1l_opy_
    global bstack1l1l1lllll_opy_
    bstack1l11lll1l_opy_ = framework_name
    logger.info(bstack11l1l1ll1l_opy_.format(bstack1l11lll1l_opy_.split(bstack11l1l11_opy_ (u"ࠬ࠳ࠧ⁗"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111l1ll_opy_():
            Service.start = bstack11ll1ll1_opy_
            Service.stop = bstack1ll1llll1l_opy_
            webdriver.Remote.get = bstack11lll1ll1_opy_
            webdriver.Remote.__init__ = bstack1lll111lll_opy_
            if not isinstance(os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ⁘")), str):
                return
            WebDriver.close = bstack1l11l1l1_opy_
            WebDriver.quit = bstack111l1l11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack11lll111l1_opy_.on():
            webdriver.Remote.__init__ = bstack1llll1ll_opy_
        bstack1l1l1lllll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11l1l11_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ⁙")):
        bstack1l1l1lllll_opy_ = eval(os.environ.get(bstack11l1l11_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭⁚")))
    if not bstack1l1l1lllll_opy_:
        bstack11lll1ll1l_opy_(bstack11l1l11_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ⁛"), bstack1l11l1111l_opy_)
    if bstack11ll111l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1ll1111l11_opy_ = bstack1l1ll1111_opy_
        except Exception as e:
            logger.error(bstack111l1llll_opy_.format(str(e)))
    if bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⁜") in str(framework_name).lower():
        if not bstack1ll1111l1ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111lllll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll111l11_opy_
            Config.getoption = bstack1l1lll11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1ll1ll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1ll1l11_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack111l1l11l_opy_(self):
    global bstack1l11lll1l_opy_
    global bstack1lll11111_opy_
    global bstack1lllll11l1_opy_
    try:
        if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⁝") in bstack1l11lll1l_opy_ and self.session_id != None and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ⁞"), bstack11l1l11_opy_ (u"࠭ࠧ ")) != bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⁠"):
            bstack1l111l1ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⁡") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⁢")
            bstack1l111lll1_opy_(logger, True)
            if self != None:
                bstack1l1l1l11l1_opy_(self, bstack1l111l1ll_opy_, bstack11l1l11_opy_ (u"ࠪ࠰ࠥ࠭⁣").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll111111l_opy_(bstack1lll1ll1111_opy_):
            item = store.get(bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⁤"), None)
            if item is not None and bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⁥"), None):
                bstack11ll111l_opy_.bstack1lllllll1_opy_(self, bstack1l11lll1ll_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l1l11_opy_ (u"࠭ࠧ⁦")
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ⁧") + str(e))
    bstack1lllll11l1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1ll1lll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack1lll111lll_opy_(self, command_executor,
             desired_capabilities=None, bstack11llll11l1_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll11111_opy_
    global bstack11l1l1lll_opy_
    global bstack111lll11_opy_
    global bstack1l11lll1l_opy_
    global bstack1lll1l1l_opy_
    global bstack1l11ll11l1_opy_
    global bstack1111l1l1_opy_
    global bstack11l1ll1l1_opy_
    global bstack1l11lll1ll_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⁨")] = str(bstack1l11lll1l_opy_) + str(__version__)
    command_executor = bstack11111l1l_opy_(bstack1111l1l1_opy_, CONFIG)
    logger.debug(bstack1l11ll11ll_opy_.format(command_executor))
    proxy = bstack1l11l1ll1l_opy_(CONFIG, proxy)
    bstack1l1l1l111_opy_ = 0
    try:
        if bstack111lll11_opy_ is True:
            bstack1l1l1l111_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⁩")))
    except:
        bstack1l1l1l111_opy_ = 0
    bstack11lllll11l_opy_ = bstack1lll111ll1_opy_(CONFIG, bstack1l1l1l111_opy_)
    logger.debug(bstack111l11l1_opy_.format(str(bstack11lllll11l_opy_)))
    bstack1l11lll1ll_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⁪"))[bstack1l1l1l111_opy_]
    if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⁫") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⁬")]:
        bstack1ll11l1l1l_opy_(bstack11lllll11l_opy_, bstack11l1ll1l1_opy_)
    if bstack1l1l1l1ll1_opy_.bstack1l1l1l1l_opy_(CONFIG, bstack1l1l1l111_opy_) and bstack1l1l1l1ll1_opy_.bstack111l1111l_opy_(bstack11lllll11l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll111111l_opy_(bstack1lll1ll1111_opy_):
            bstack1l1l1l1ll1_opy_.set_capabilities(bstack11lllll11l_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1lll1ll1_opy_ = bstack1l1lll11l_opy_(desired_capabilities)
        bstack1l1lll1ll1_opy_[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⁭")] = bstack11l1l1l11l_opy_(CONFIG)
        bstack1ll1lll11l_opy_ = bstack1lll111ll1_opy_(bstack1l1lll1ll1_opy_)
        if bstack1ll1lll11l_opy_:
            bstack11lllll11l_opy_ = update(bstack1ll1lll11l_opy_, bstack11lllll11l_opy_)
        desired_capabilities = None
    if options:
        bstack11l11ll1ll_opy_(options, bstack11lllll11l_opy_)
    if not options:
        options = bstack1l11111l11_opy_(bstack11lllll11l_opy_)
    if proxy and bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⁮")):
        options.proxy(proxy)
    if options and bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⁯")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1lllll_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⁰")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11lllll11l_opy_)
    logger.info(bstack11l1ll1ll_opy_)
    bstack1l1ll1l11l_opy_.end(EVENTS.bstack1l1l11l1l1_opy_.value, EVENTS.bstack1l1l11l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥⁱ"),
                               EVENTS.bstack1l1l11l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⁲"), True, None)
    if bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ⁳")):
        bstack1lll1l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⁴")):
        bstack1lll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ⁵")):
        bstack1lll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11llll11l1_opy_=bstack11llll11l1_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l11ll1111_opy_ = bstack11l1l11_opy_ (u"ࠨࠩ⁶")
        if bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ⁷")):
            bstack1l11ll1111_opy_ = self.caps.get(bstack11l1l11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⁸"))
        else:
            bstack1l11ll1111_opy_ = self.capabilities.get(bstack11l1l11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⁹"))
        if bstack1l11ll1111_opy_:
            bstack1l11llll_opy_(bstack1l11ll1111_opy_)
            if bstack1ll1lllll_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ⁺")):
                self.command_executor._url = bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⁻") + bstack1111l1l1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ⁼")
            else:
                self.command_executor._url = bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ⁽") + bstack1l11ll1111_opy_ + bstack11l1l11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ⁾")
            logger.debug(bstack1111llll_opy_.format(bstack1l11ll1111_opy_))
        else:
            logger.debug(bstack11ll1l1111_opy_.format(bstack11l1l11_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦⁿ")))
    except Exception as e:
        logger.debug(bstack11ll1l1111_opy_.format(e))
    bstack1lll11111_opy_ = self.session_id
    if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ₀") in bstack1l11lll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ₁"), None)
        if item:
            bstack1111ll1lll1_opy_ = getattr(item, bstack11l1l11_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫ₂"), False)
            if not getattr(item, bstack11l1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ₃"), None) and bstack1111ll1lll1_opy_:
                setattr(store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ₄")], bstack11l1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ₅"), self)
        bstack1ll11111l1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ₆"), None)
        if bstack1ll11111l1_opy_ and bstack1ll11111l1_opy_.get(bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ₇"), bstack11l1l11_opy_ (u"ࠬ࠭₈")) == bstack11l1l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ₉"):
            bstack11lll111l1_opy_.bstack11ll1111_opy_(self)
    bstack1l11ll11l1_opy_.append(self)
    if bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ₊") in CONFIG and bstack11l1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭₋") in CONFIG[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ₌")][bstack1l1l1l111_opy_]:
        bstack11l1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭₍")][bstack1l1l1l111_opy_][bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ₎")]
    logger.debug(bstack111111ll_opy_.format(bstack1lll11111_opy_))
@measure(event_name=EVENTS.bstack11lll1l111_opy_, stage=STAGE.bstack1l1ll1lll_opy_, bstack11ll11ll11_opy_=bstack11l1l1lll_opy_)
def bstack11lll1ll1_opy_(self, url):
    global bstack1l1l1lll_opy_
    global CONFIG
    try:
        bstack1l1ll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1ll111l_opy_.format(str(err)))
    try:
        bstack1l1l1lll_opy_(self, url)
    except Exception as e:
        try:
            bstack1111l1lll_opy_ = str(e)
            if any(err_msg in bstack1111l1lll_opy_ for err_msg in bstack1111lll11_opy_):
                bstack1l1ll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1ll111l_opy_.format(str(err)))
        raise e
def bstack1ll1ll11ll_opy_(item, when):
    global bstack1l1111ll1l_opy_
    try:
        bstack1l1111ll1l_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1ll1ll1_opy_(item, call, rep):
    global bstack11ll11lll_opy_
    global bstack1l11ll11l1_opy_
    name = bstack11l1l11_opy_ (u"ࠬ࠭₏")
    try:
        if rep.when == bstack11l1l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫₐ"):
            bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
            bstack111l1111l1l_opy_ = item.config.getoption(bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩₑ"))
            try:
                if (str(bstack111l1111l1l_opy_).lower() != bstack11l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ₒ")):
                    name = str(rep.nodeid)
                    bstack1l11lll111_opy_ = bstack11ll11111_opy_(bstack11l1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪₓ"), name, bstack11l1l11_opy_ (u"ࠪࠫₔ"), bstack11l1l11_opy_ (u"ࠫࠬₕ"), bstack11l1l11_opy_ (u"ࠬ࠭ₖ"), bstack11l1l11_opy_ (u"࠭ࠧₗ"))
                    os.environ[bstack11l1l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪₘ")] = name
                    for driver in bstack1l11ll11l1_opy_:
                        if bstack1lll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11lll111_opy_)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨₙ").format(str(e)))
            try:
                bstack111l1l1l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪₚ"):
                    status = bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪₛ") if rep.outcome.lower() == bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫₜ") else bstack11l1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ₝")
                    reason = bstack11l1l11_opy_ (u"࠭ࠧ₞")
                    if status == bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ₟"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭₠") if status == bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ₡") else bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ₢")
                    data = name + bstack11l1l11_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭₣") if status == bstack11l1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ₤") else name + bstack11l1l11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ₥") + reason
                    bstack11l1l11l1l_opy_ = bstack11ll11111_opy_(bstack11l1l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ₦"), bstack11l1l11_opy_ (u"ࠨࠩ₧"), bstack11l1l11_opy_ (u"ࠩࠪ₨"), bstack11l1l11_opy_ (u"ࠪࠫ₩"), level, data)
                    for driver in bstack1l11ll11l1_opy_:
                        if bstack1lll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1l11l1l_opy_)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ₪").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ₫").format(str(e)))
    bstack11ll11lll_opy_(item, call, rep)
notset = Notset()
def bstack1l1lll11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11llll11ll_opy_
    if str(name).lower() == bstack11l1l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭€"):
        return bstack11l1l11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ₭")
    else:
        return bstack11llll11ll_opy_(self, name, default, skip)
def bstack1l1ll1111_opy_(self):
    global CONFIG
    global bstack1ll111l1_opy_
    try:
        proxy = bstack11ll1l1l1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1l11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭₮")):
                proxies = bstack11llll1l_opy_(proxy, bstack11111l1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111111ll_opy_ = proxies.popitem()
                    if bstack11l1l11_opy_ (u"ࠤ࠽࠳࠴ࠨ₯") in bstack1l111111ll_opy_:
                        return bstack1l111111ll_opy_
                    else:
                        return bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ₰") + bstack1l111111ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣ₱").format(str(e)))
    return bstack1ll111l1_opy_(self)
def bstack11ll111l1_opy_():
    return (bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ₲") in CONFIG or bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ₳") in CONFIG) and bstack1lll1l1ll1_opy_() and bstack1ll1lllll_opy_() >= version.parse(
        bstack11lllll11_opy_)
def bstack1ll11llll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11l1l1lll_opy_
    global bstack111lll11_opy_
    global bstack1l11lll1l_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ₴")] = str(bstack1l11lll1l_opy_) + str(__version__)
    bstack1l1l1l111_opy_ = 0
    try:
        if bstack111lll11_opy_ is True:
            bstack1l1l1l111_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ₵")))
    except:
        bstack1l1l1l111_opy_ = 0
    CONFIG[bstack11l1l11_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ₶")] = True
    bstack11lllll11l_opy_ = bstack1lll111ll1_opy_(CONFIG, bstack1l1l1l111_opy_)
    logger.debug(bstack111l11l1_opy_.format(str(bstack11lllll11l_opy_)))
    if CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ₷")):
        bstack1ll11l1l1l_opy_(bstack11lllll11l_opy_, bstack11l1ll1l1_opy_)
    if bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ₸") in CONFIG and bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ₹") in CONFIG[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ₺")][bstack1l1l1l111_opy_]:
        bstack11l1l1lll_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ₻")][bstack1l1l1l111_opy_][bstack11l1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭₼")]
    import urllib
    import json
    if bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭₽") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ₾")]).lower() != bstack11l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ₿"):
        bstack1l1l11llll_opy_ = bstack1lll11ll_opy_()
        bstack1l1lllll_opy_ = bstack1l1l11llll_opy_ + urllib.parse.quote(json.dumps(bstack11lllll11l_opy_))
    else:
        bstack1l1lllll_opy_ = bstack11l1l11_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ⃀") + urllib.parse.quote(json.dumps(bstack11lllll11l_opy_))
    browser = self.connect(bstack1l1lllll_opy_)
    return browser
def bstack1111l1ll1_opy_():
    global bstack1l1l1lllll_opy_
    global bstack1l11lll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11llll111_opy_
        if not bstack1ll1111l1ll_opy_():
            global bstack1l1l11l11_opy_
            if not bstack1l1l11l11_opy_:
                from bstack_utils.helper import bstack1lll1l1l1l_opy_, bstack11lllll1l_opy_
                bstack1l1l11l11_opy_ = bstack1lll1l1l1l_opy_()
                bstack11lllll1l_opy_(bstack1l11lll1l_opy_)
            BrowserType.connect = bstack11llll111_opy_
            return
        BrowserType.launch = bstack1ll11llll_opy_
        bstack1l1l1lllll_opy_ = True
    except Exception as e:
        pass
def bstack111l11111ll_opy_():
    global CONFIG
    global bstack11ll11l11l_opy_
    global bstack1111l1l1_opy_
    global bstack11l1ll1l1_opy_
    global bstack111lll11_opy_
    global bstack1llll1ll1l_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ⃁")))
    bstack11ll11l11l_opy_ = eval(os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ⃂")))
    bstack1111l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ⃃"))
    bstack1lll11ll11_opy_(CONFIG, bstack11ll11l11l_opy_)
    bstack1llll1ll1l_opy_ = bstack111ll1l11_opy_.bstack11ll1l111l_opy_(CONFIG, bstack1llll1ll1l_opy_)
    if cli.bstack11llll1l1_opy_():
        bstack11l11ll11l_opy_.invoke(bstack1llll111ll_opy_.CONNECT, bstack111111ll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⃄"), bstack11l1l11_opy_ (u"ࠪ࠴ࠬ⃅")))
        cli.bstack1llll1l1111_opy_(cli_context.platform_index)
        cli.bstack1llll11l111_opy_(bstack11111l1l_opy_(bstack1111l1l1_opy_, CONFIG), cli_context.platform_index, bstack1l11111l11_opy_)
        cli.bstack1lll1lllll1_opy_()
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ⃆") + str(cli_context.platform_index) + bstack11l1l11_opy_ (u"ࠧࠨ⃇"))
        return # skip all existing bstack111l111l11l_opy_
    global bstack1lll1l1l_opy_
    global bstack1lllll11l1_opy_
    global bstack1l1llll11_opy_
    global bstack1lll11l1ll_opy_
    global bstack1ll111ll_opy_
    global bstack1l111l1l1_opy_
    global bstack1llll1l1ll_opy_
    global bstack1l1l1lll_opy_
    global bstack1ll111l1_opy_
    global bstack11llll11ll_opy_
    global bstack1l1111ll1l_opy_
    global bstack11ll11lll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll1l1l_opy_ = webdriver.Remote.__init__
        bstack1lllll11l1_opy_ = WebDriver.quit
        bstack1llll1l1ll_opy_ = WebDriver.close
        bstack1l1l1lll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⃈") in CONFIG or bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⃉") in CONFIG) and bstack1lll1l1ll1_opy_():
        if bstack1ll1lllll_opy_() < version.parse(bstack11lllll11_opy_):
            logger.error(bstack1lll1l1ll_opy_.format(bstack1ll1lllll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll111l1_opy_ = RemoteConnection._1ll1111l11_opy_
            except Exception as e:
                logger.error(bstack111l1llll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11llll11ll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1111ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1ll11lllll_opy_)
    try:
        from pytest_bdd import reporting
        bstack11ll11lll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ⃊"))
    bstack11l1ll1l1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭⃋"), {}).get(bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⃌"))
    bstack111lll11_opy_ = True
    bstack1l1111l11l_opy_(bstack1111111ll_opy_)
if (bstack11ll1ll1111_opy_()):
    bstack111l11111ll_opy_()
@bstack111ll1l1l1_opy_(class_method=False)
def bstack1111ll1l1ll_opy_(hook_name, event, bstack1l11l1l1l11_opy_=None):
    if hook_name not in [bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⃍"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⃎"), bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⃏"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⃐"), bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⃑"), bstack11l1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵ⃒ࠪ"), bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥ⃓ࠩ"), bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⃔")]:
        return
    node = store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⃕")]
    if hook_name in [bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⃖"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⃗")]:
        node = store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳ⃘ࠧ")]
    elif hook_name in [bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹ⃙ࠧ"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶ⃚ࠫ")]:
        node = store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⃛")]
    hook_type = bstack111lll111ll_opy_(hook_name)
    if event == bstack11l1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⃜"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_[hook_type], bstack1lll111lll1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l1lll_opy_ = {
            bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⃝"): uuid,
            bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⃞"): bstack1ll11ll11_opy_(),
            bstack11l1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⃟"): bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⃠"),
            bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⃡"): hook_type,
            bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⃢"): hook_name
        }
        store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⃣")].append(uuid)
        bstack111l1111l11_opy_ = node.nodeid
        if hook_type == bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⃤"):
            if not _111ll1l1ll_opy_.get(bstack111l1111l11_opy_, None):
                _111ll1l1ll_opy_[bstack111l1111l11_opy_] = {bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ⃥࠭"): []}
            _111ll1l1ll_opy_[bstack111l1111l11_opy_][bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹ⃦ࠧ")].append(bstack111l1l1lll_opy_[bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⃧")])
        _111ll1l1ll_opy_[bstack111l1111l11_opy_ + bstack11l1l11_opy_ (u"ࠪ࠱⃨ࠬ") + hook_name] = bstack111l1l1lll_opy_
        bstack111l111l111_opy_(node, bstack111l1l1lll_opy_, bstack11l1l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⃩"))
    elif event == bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵ⃪ࠫ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llllll1lll_opy_[hook_type], bstack1lll111lll1_opy_.POST, node, None, bstack1l11l1l1l11_opy_)
            return
        bstack11l111l111_opy_ = node.nodeid + bstack11l1l11_opy_ (u"࠭࠭ࠨ⃫") + hook_name
        _111ll1l1ll_opy_[bstack11l111l111_opy_][bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸ⃬ࠬ")] = bstack1ll11ll11_opy_()
        bstack1111llll111_opy_(_111ll1l1ll_opy_[bstack11l111l111_opy_][bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ⃭࠭")])
        bstack111l111l111_opy_(node, _111ll1l1ll_opy_[bstack11l111l111_opy_], bstack11l1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧ⃮ࠫ"), bstack1111ll1ll1l_opy_=bstack1l11l1l1l11_opy_)
def bstack1111ll1llll_opy_():
    global bstack1111lll1ll1_opy_
    if bstack1lll1ll11l_opy_():
        bstack1111lll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪ⃯ࠧ")
    else:
        bstack1111lll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⃰")
@bstack11lll111l1_opy_.bstack111l1l11111_opy_
def bstack1111lll111l_opy_():
    bstack1111ll1llll_opy_()
    if cli.is_running():
        try:
            bstack11l1ll1ll1l_opy_(bstack1111ll1l1ll_opy_)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ⃱").format(e))
        return
    if bstack1lll1l1ll1_opy_():
        bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
        bstack11l1l11_opy_ (u"࠭ࠧࠨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡ࠿ࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤ࡬࡫ࡴࡴࠢࡸࡷࡪࡪࠠࡧࡱࡵࠤࡦ࠷࠱ࡺࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠱ࡼࡸࡡࡱࡲ࡬ࡲ࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡷࠤ࡮ࡹࠠࡱࡣࡷࡧ࡭࡫ࡤࠡ࡫ࡱࠤࡦࠦࡤࡪࡨࡩࡩࡷ࡫࡮ࡵࠢࡳࡶࡴࡩࡥࡴࡵࠣ࡭ࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡵࡴࠢࡺࡩࠥࡴࡥࡦࡦࠣࡸࡴࠦࡵࡴࡧࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡕࡧࡴࡤࡪࠫࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡮ࡡ࡯ࡦ࡯ࡩࡷ࠯ࠠࡧࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠧࠨࠩ⃲")
        if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⃳")):
            if CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⃴")) is not None and int(CONFIG[bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⃵")]) > 1:
                bstack1ll111l1l_opy_(bstack1ll11ll1_opy_)
            return
        bstack1ll111l1l_opy_(bstack1ll11ll1_opy_)
    try:
        bstack11l1ll1ll1l_opy_(bstack1111ll1l1ll_opy_)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⃶").format(e))
bstack1111lll111l_opy_()