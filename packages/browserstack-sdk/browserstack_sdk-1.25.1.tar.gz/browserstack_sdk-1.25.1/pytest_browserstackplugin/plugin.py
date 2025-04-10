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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l111l1111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1l1l11l1_opy_, bstack11l1111ll_opy_, update, bstack1l111ll111_opy_,
                                       bstack1l1l1lll1l_opy_, bstack11l1l111l1_opy_, bstack1111lll1l_opy_, bstack1ll11ll1l_opy_,
                                       bstack1llll1111_opy_, bstack1ll11ll1ll_opy_, bstack11llll11l1_opy_, bstack1l11llll11_opy_,
                                       bstack11lll11lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1lllll1l11_opy_)
from browserstack_sdk.bstack1ll11l1l1l_opy_ import bstack1111l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1ll1111l_opy_
from bstack_utils.capture import bstack11l111l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll111lll1_opy_, bstack1111lll11_opy_, bstack1l111l11ll_opy_, \
    bstack1l1111l1_opy_
from bstack_utils.helper import bstack11111l111_opy_, bstack11l1l1l1ll1_opy_, bstack111l1l1ll1_opy_, bstack11llllll_opy_, bstack1l1llll11ll_opy_, bstack11l1ll11ll_opy_, \
    bstack11l1llll1ll_opy_, \
    bstack11l1l111111_opy_, bstack11ll1llll1_opy_, bstack1llllll1ll_opy_, bstack11ll11l1l11_opy_, bstack111111111_opy_, Notset, \
    bstack1l11111lll_opy_, bstack11l1ll11lll_opy_, bstack11ll1111l1l_opy_, Result, bstack11l1l1l1l11_opy_, bstack11l1l11ll1l_opy_, bstack111ll11ll1_opy_, \
    bstack11l1l1l11l_opy_, bstack1ll1lll11_opy_, bstack11l11l1ll_opy_, bstack11l1l1lllll_opy_
from bstack_utils.bstack11l11l1lll1_opy_ import bstack11l11ll1l1l_opy_
from bstack_utils.messages import bstack1l1l1lll1_opy_, bstack1ll1l1l1_opy_, bstack1111l11ll_opy_, bstack11lll11l11_opy_, bstack11ll1111ll_opy_, \
    bstack11lll111ll_opy_, bstack11l1l111l_opy_, bstack11ll1l1lll_opy_, bstack1l11111111_opy_, bstack11111lll1_opy_, \
    bstack11lll111_opy_, bstack11l11ll11l_opy_
from bstack_utils.proxy import bstack11ll11l1_opy_, bstack1l1111l1l_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack111l1l1l11l_opy_, bstack111l1ll1111_opy_, bstack111l1l1lll1_opy_, bstack111l1l1l1l1_opy_, \
    bstack111l1l1llll_opy_, bstack111l1l1ll11_opy_, bstack111l1ll11l1_opy_, bstack1ll1llll1l_opy_, bstack111l1ll111l_opy_
from bstack_utils.bstack1l1l1llll_opy_ import bstack11ll1l1l_opy_
from bstack_utils.bstack1l1lllll_opy_ import bstack11ll1ll111_opy_, bstack111ll111l_opy_, bstack1l111ll1_opy_, \
    bstack111l1l1l_opy_, bstack11lllll11l_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack11l11111l1_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11l1ll1ll_opy_
import bstack_utils.accessibility as bstack1l11llll_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack1l1lll1lll_opy_
from bstack_utils.bstack1ll1l11l1l_opy_ import bstack1ll1l11l1l_opy_
from browserstack_sdk.__init__ import bstack11ll11111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111lll_opy_ import bstack1lll1111l11_opy_
from browserstack_sdk.sdk_cli.bstack1111111l_opy_ import bstack1111111l_opy_, bstack1l1111ll1l_opy_, bstack11111111l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111lll1l1_opy_, bstack1lllllll1ll_opy_, bstack1lll1l11l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111111l_opy_ import bstack1111111l_opy_, bstack1l1111ll1l_opy_, bstack11111111l_opy_
bstack1lll111l1_opy_ = None
bstack1l1llll11_opy_ = None
bstack111lllll1_opy_ = None
bstack1l111llll_opy_ = None
bstack11l1l1ll_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1lll1l1lll_opy_ = None
bstack11l111ll1_opy_ = None
bstack11lll1ll11_opy_ = None
bstack11l1ll1l11_opy_ = None
bstack11lllll1_opy_ = None
bstack1llll1l1l_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1l111l1l1l_opy_ = bstack1ll1l1_opy_ (u"ࠪࠫὄ")
CONFIG = {}
bstack1l1111lll1_opy_ = False
bstack1l11ll1ll1_opy_ = bstack1ll1l1_opy_ (u"ࠫࠬὅ")
bstack11lll11l_opy_ = bstack1ll1l1_opy_ (u"ࠬ࠭὆")
bstack1ll1l11l_opy_ = False
bstack1l1ll1ll11_opy_ = []
bstack1l1111l1l1_opy_ = bstack1ll111lll1_opy_
bstack11111lll1l1_opy_ = bstack1ll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭὇")
bstack111lll1l_opy_ = {}
bstack1l1111l111_opy_ = None
bstack11111l1l1_opy_ = False
logger = bstack1l1ll1111l_opy_.get_logger(__name__, bstack1l1111l1l1_opy_)
store = {
    bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫὈ"): []
}
bstack1111l11llll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11l11l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111lll1l1_opy_(
    test_framework_name=bstack1llll11l1_opy_[bstack1ll1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬὉ")] if bstack111111111_opy_() else bstack1llll11l1_opy_[bstack1ll1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩὊ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1lllll11ll_opy_(page, bstack1l1ll1l1l_opy_):
    try:
        page.evaluate(bstack1ll1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦὋ"),
                      bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨὌ") + json.dumps(
                          bstack1l1ll1l1l_opy_) + bstack1ll1l1_opy_ (u"ࠧࢃࡽࠣὍ"))
    except Exception as e:
        print(bstack1ll1l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦ὎"), e)
def bstack11llll111l_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ὏"), bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ὐ") + json.dumps(
            message) + bstack1ll1l1_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬὑ") + json.dumps(level) + bstack1ll1l1_opy_ (u"ࠪࢁࢂ࠭ὒ"))
    except Exception as e:
        print(bstack1ll1l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢὓ"), e)
def pytest_configure(config):
    global bstack1l11ll1ll1_opy_
    global CONFIG
    bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
    config.args = bstack11l1ll1ll_opy_.bstack1111l1l1l11_opy_(config.args)
    bstack11ll11ll_opy_.bstack1l1ll1111_opy_(bstack11l11l1ll_opy_(config.getoption(bstack1ll1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩὔ"))))
    try:
        bstack1l1ll1111l_opy_.bstack11l11l11l1l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1111111l_opy_.invoke(bstack1l1111ll1l_opy_.CONNECT, bstack11111111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ὕ"), bstack1ll1l1_opy_ (u"ࠧ࠱ࠩὖ")))
        config = json.loads(os.environ.get(bstack1ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢὗ"), bstack1ll1l1_opy_ (u"ࠤࡾࢁࠧ὘")))
        cli.bstack1lll1l1l1ll_opy_(bstack1llllll1ll_opy_(bstack1l11ll1ll1_opy_, CONFIG), cli_context.platform_index, bstack1l111ll111_opy_)
    if cli.bstack1lllll11l11_opy_(bstack1lll1111l11_opy_):
        cli.bstack1llll11111l_opy_()
        logger.debug(bstack1ll1l1_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤὙ") + str(cli_context.platform_index) + bstack1ll1l1_opy_ (u"ࠦࠧ὚"))
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.BEFORE_ALL, bstack1lll1l11l1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1ll1l1_opy_ (u"ࠧࡽࡨࡦࡰࠥὛ"), None)
    if cli.is_running() and when == bstack1ll1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ὜"):
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.LOG_REPORT, bstack1lll1l11l1l_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1ll1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨὝ"):
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.BEFORE_EACH, bstack1lll1l11l1l_opy_.POST, item, call, outcome)
        elif when == bstack1ll1l1_opy_ (u"ࠣࡥࡤࡰࡱࠨ὞"):
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.LOG_REPORT, bstack1lll1l11l1l_opy_.POST, item, call, outcome)
        elif when == bstack1ll1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦὟ"):
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.AFTER_EACH, bstack1lll1l11l1l_opy_.POST, item, call, outcome)
        return # skip all existing bstack11111llllll_opy_
    bstack11111lll1ll_opy_ = item.config.getoption(bstack1ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬὠ"))
    plugins = item.config.getoption(bstack1ll1l1_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧὡ"))
    report = outcome.get_result()
    bstack1111l11l11l_opy_(item, call, report)
    if bstack1ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥὢ") not in plugins or bstack111111111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1l1_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢὣ"), None)
    page = getattr(item, bstack1ll1l1_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨὤ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1111l1111l1_opy_(item, report, summary, bstack11111lll1ll_opy_)
    if (page is not None):
        bstack11111lllll1_opy_(item, report, summary, bstack11111lll1ll_opy_)
def bstack1111l1111l1_opy_(item, report, summary, bstack11111lll1ll_opy_):
    if report.when == bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧὥ") and report.skipped:
        bstack111l1ll111l_opy_(report)
    if report.when in [bstack1ll1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣὦ"), bstack1ll1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧὧ")]:
        return
    if not bstack1l1llll11ll_opy_():
        return
    try:
        if (str(bstack11111lll1ll_opy_).lower() != bstack1ll1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩὨ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪὩ") + json.dumps(
                    report.nodeid) + bstack1ll1l1_opy_ (u"࠭ࡽࡾࠩὪ"))
        os.environ[bstack1ll1l1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪὫ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣὬ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦὭ")))
    bstack111l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠥࠦὮ")
    bstack111l1ll111l_opy_(report)
    if not passed:
        try:
            bstack111l11ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦὯ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111l11ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢὰ")))
        bstack111l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࠢά")
        if not passed:
            try:
                bstack111l11ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢὲ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111l11ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬέ")
                    + json.dumps(bstack1ll1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥὴ"))
                    + bstack1ll1l1_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨή")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩὶ")
                    + json.dumps(str(bstack111l11ll_opy_))
                    + bstack1ll1l1_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣί")
                )
        except Exception as e:
            summary.append(bstack1ll1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦὸ").format(e))
def bstack1111l11l111_opy_(test_name, error_message):
    try:
        bstack1111l11ll1l_opy_ = []
        bstack1lll1l111_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧό"), bstack1ll1l1_opy_ (u"ࠨ࠲ࠪὺ"))
        bstack11l11lll11_opy_ = {bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧύ"): test_name, bstack1ll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩὼ"): error_message, bstack1ll1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪώ"): bstack1lll1l111_opy_}
        bstack11111llll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l1_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ὾"))
        if os.path.exists(bstack11111llll1l_opy_):
            with open(bstack11111llll1l_opy_) as f:
                bstack1111l11ll1l_opy_ = json.load(f)
        bstack1111l11ll1l_opy_.append(bstack11l11lll11_opy_)
        with open(bstack11111llll1l_opy_, bstack1ll1l1_opy_ (u"࠭ࡷࠨ὿")) as f:
            json.dump(bstack1111l11ll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᾀ") + str(e))
def bstack11111lllll1_opy_(item, report, summary, bstack11111lll1ll_opy_):
    if report.when in [bstack1ll1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᾁ"), bstack1ll1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᾂ")]:
        return
    if (str(bstack11111lll1ll_opy_).lower() != bstack1ll1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᾃ")):
        bstack1lllll11ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᾄ")))
    bstack111l11ll_opy_ = bstack1ll1l1_opy_ (u"ࠧࠨᾅ")
    bstack111l1ll111l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111l11ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᾆ").format(e)
                )
        try:
            if passed:
                bstack11lllll11l_opy_(getattr(item, bstack1ll1l1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᾇ"), None), bstack1ll1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᾈ"))
            else:
                error_message = bstack1ll1l1_opy_ (u"ࠩࠪᾉ")
                if bstack111l11ll_opy_:
                    bstack11llll111l_opy_(item._page, str(bstack111l11ll_opy_), bstack1ll1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᾊ"))
                    bstack11lllll11l_opy_(getattr(item, bstack1ll1l1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᾋ"), None), bstack1ll1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᾌ"), str(bstack111l11ll_opy_))
                    error_message = str(bstack111l11ll_opy_)
                else:
                    bstack11lllll11l_opy_(getattr(item, bstack1ll1l1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᾍ"), None), bstack1ll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᾎ"))
                bstack1111l11l111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᾏ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1ll1l1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᾐ"), default=bstack1ll1l1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᾑ"), help=bstack1ll1l1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᾒ"))
    parser.addoption(bstack1ll1l1_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᾓ"), default=bstack1ll1l1_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᾔ"), help=bstack1ll1l1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᾕ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1l1_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᾖ"), action=bstack1ll1l1_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᾗ"), default=bstack1ll1l1_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᾘ"),
                         help=bstack1ll1l1_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᾙ"))
def bstack11l11l1111_opy_(log):
    if not (log[bstack1ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᾚ")] and log[bstack1ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᾛ")].strip()):
        return
    active = bstack11l111ll11_opy_()
    log = {
        bstack1ll1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᾜ"): log[bstack1ll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᾝ")],
        bstack1ll1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᾞ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l1_opy_ (u"ࠪ࡞ࠬᾟ"),
        bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᾠ"): log[bstack1ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᾡ")],
    }
    if active:
        if active[bstack1ll1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᾢ")] == bstack1ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᾣ"):
            log[bstack1ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾤ")] = active[bstack1ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾥ")]
        elif active[bstack1ll1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨᾦ")] == bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᾧ"):
            log[bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾨ")] = active[bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾩ")]
    bstack1l1lll1lll_opy_.bstack1l111lll1_opy_([log])
def bstack11l111ll11_opy_():
    if len(store[bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᾪ")]) > 0 and store[bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᾫ")][-1]:
        return {
            bstack1ll1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᾬ"): bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᾭ"),
            bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾮ"): store[bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᾯ")][-1]
        }
    if store.get(bstack1ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᾰ"), None):
        return {
            bstack1ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬᾱ"): bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᾲ"),
            bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾳ"): store[bstack1ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᾴ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.INIT_TEST, bstack1lll1l11l1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.INIT_TEST, bstack1lll1l11l1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1111l1111ll_opy_ = True
        bstack1ll11ll1l1_opy_ = bstack1l11llll_opy_.bstack1ll11l1ll_opy_(bstack11l1l111111_opy_(item.own_markers))
        if not cli.bstack1lllll11l11_opy_(bstack1lll1111l11_opy_):
            item._a11y_test_case = bstack1ll11ll1l1_opy_
            if bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᾵"), None):
                driver = getattr(item, bstack1ll1l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᾶ"), None)
                item._a11y_started = bstack1l11llll_opy_.bstack11llll11_opy_(driver, bstack1ll11ll1l1_opy_)
        if not bstack1l1lll1lll_opy_.on() or bstack11111lll1l1_opy_ != bstack1ll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᾷ"):
            return
        global current_test_uuid #, bstack11l11111ll_opy_
        bstack111l1lll1l_opy_ = {
            bstack1ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᾸ"): uuid4().__str__(),
            bstack1ll1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᾹ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l1_opy_ (u"ࠩ࡝ࠫᾺ")
        }
        current_test_uuid = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨΆ")]
        store[bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᾼ")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ᾽")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11l11l_opy_[item.nodeid] = {**_111l11l11l_opy_[item.nodeid], **bstack111l1lll1l_opy_}
        bstack11111llll11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack1ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧι"))
    except Exception as err:
        print(bstack1ll1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩ᾿"), str(err))
def pytest_runtest_setup(item):
    store[bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ῀")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.BEFORE_EACH, bstack1lll1l11l1l_opy_.PRE, item, bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ῁"))
        return # skip all existing bstack11111llllll_opy_
    global bstack1111l11llll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11l1l11_opy_():
        atexit.register(bstack1ll1l111l1_opy_)
        if not bstack1111l11llll_opy_:
            try:
                bstack1111l11l1ll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1lllll_opy_():
                    bstack1111l11l1ll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1111l11l1ll_opy_:
                    signal.signal(s, bstack1111l11111l_opy_)
                bstack1111l11llll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦῂ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l1l11l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫῃ")
    try:
        if not bstack1l1lll1lll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1lll1l_opy_ = {
            bstack1ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪῄ"): uuid,
            bstack1ll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ῅"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l1_opy_ (u"࡛ࠧࠩῆ"),
            bstack1ll1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ῇ"): bstack1ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧῈ"),
            bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭Έ"): bstack1ll1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩῊ"),
            bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨΉ"): bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬῌ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ῍")] = item
        store[bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ῎")] = [uuid]
        if not _111l11l11l_opy_.get(item.nodeid, None):
            _111l11l11l_opy_[item.nodeid] = {bstack1ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ῏"): [], bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬῐ"): []}
        _111l11l11l_opy_[item.nodeid][bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪῑ")].append(bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪῒ")])
        _111l11l11l_opy_[item.nodeid + bstack1ll1l1_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭ΐ")] = bstack111l1lll1l_opy_
        bstack11111ll1ll1_opy_(item, bstack111l1lll1l_opy_, bstack1ll1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ῔"))
    except Exception as err:
        print(bstack1ll1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ῕"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.AFTER_EACH, bstack1lll1l11l1l_opy_.PRE, item, bstack1ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫῖ"))
        return # skip all existing bstack11111llllll_opy_
    try:
        global bstack111lll1l_opy_
        bstack1lll1l111_opy_ = 0
        if bstack1ll1l11l_opy_ is True:
            bstack1lll1l111_opy_ = int(os.environ.get(bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪῗ")))
        if bstack1l1l11l1l_opy_.bstack1111l1l1_opy_() == bstack1ll1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤῘ"):
            if bstack1l1l11l1l_opy_.bstack11l11111_opy_() == bstack1ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢῙ"):
                bstack11111ll1lll_opy_ = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩῚ"), None)
                bstack11ll1l1ll_opy_ = bstack11111ll1lll_opy_ + bstack1ll1l1_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥΊ")
                driver = getattr(item, bstack1ll1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ῜"), None)
                bstack11l1ll11l_opy_ = getattr(item, bstack1ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ῝"), None)
                bstack1l1ll11lll_opy_ = getattr(item, bstack1ll1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ῞"), None)
                PercySDK.screenshot(driver, bstack11ll1l1ll_opy_, bstack11l1ll11l_opy_=bstack11l1ll11l_opy_, bstack1l1ll11lll_opy_=bstack1l1ll11lll_opy_, bstack1ll11111l_opy_=bstack1lll1l111_opy_)
        if not cli.bstack1lllll11l11_opy_(bstack1lll1111l11_opy_):
            if getattr(item, bstack1ll1l1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ῟"), False):
                bstack1111l111_opy_.bstack1ll1l11lll_opy_(getattr(item, bstack1ll1l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ῠ"), None), bstack111lll1l_opy_, logger, item)
        if not bstack1l1lll1lll_opy_.on():
            return
        bstack111l1lll1l_opy_ = {
            bstack1ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫῡ"): uuid4().__str__(),
            bstack1ll1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫῢ"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l1_opy_ (u"ࠨ࡜ࠪΰ"),
            bstack1ll1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧῤ"): bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨῥ"),
            bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧῦ"): bstack1ll1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩῧ"),
            bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩῨ"): bstack1ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩῩ")
        }
        _111l11l11l_opy_[item.nodeid + bstack1ll1l1_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫῪ")] = bstack111l1lll1l_opy_
        bstack11111ll1ll1_opy_(item, bstack111l1lll1l_opy_, bstack1ll1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪΎ"))
    except Exception as err:
        print(bstack1ll1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩῬ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l1l1l1_opy_(fixturedef.argname):
        store[bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ῭")] = request.node
    elif bstack111l1l1llll_opy_(fixturedef.argname):
        store[bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ΅")] = request.node
    if not bstack1l1lll1lll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.SETUP_FIXTURE, bstack1lll1l11l1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.SETUP_FIXTURE, bstack1lll1l11l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111llllll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.SETUP_FIXTURE, bstack1lll1l11l1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.SETUP_FIXTURE, bstack1lll1l11l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111llllll_opy_
    try:
        fixture = {
            bstack1ll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ`"): fixturedef.argname,
            bstack1ll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ῰"): bstack11l1llll1ll_opy_(outcome),
            bstack1ll1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ῱"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ῲ")]
        if not _111l11l11l_opy_.get(current_test_item.nodeid, None):
            _111l11l11l_opy_[current_test_item.nodeid] = {bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬῳ"): []}
        _111l11l11l_opy_[current_test_item.nodeid][bstack1ll1l1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ῴ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ῵"), str(err))
if bstack111111111_opy_() and bstack1l1lll1lll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.STEP, bstack1lll1l11l1l_opy_.PRE, request, step)
            return
        try:
            _111l11l11l_opy_[request.node.nodeid][bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩῶ")].bstack11lll1ll1l_opy_(id(step))
        except Exception as err:
            print(bstack1ll1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬῷ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.STEP, bstack1lll1l11l1l_opy_.POST, request, step, exception)
            return
        try:
            _111l11l11l_opy_[request.node.nodeid][bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫῸ")].bstack111llll11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭Ό"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.STEP, bstack1lll1l11l1l_opy_.POST, request, step)
            return
        try:
            bstack11l111l1ll_opy_: bstack11l11111l1_opy_ = _111l11l11l_opy_[request.node.nodeid][bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ὼ")]
            bstack11l111l1ll_opy_.bstack111llll11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨΏ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111lll1l1_opy_
        try:
            if not bstack1l1lll1lll_opy_.on() or bstack11111lll1l1_opy_ != bstack1ll1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩῼ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.TEST, bstack1lll1l11l1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ´"), None)
            if not _111l11l11l_opy_.get(request.node.nodeid, None):
                _111l11l11l_opy_[request.node.nodeid] = {}
            bstack11l111l1ll_opy_ = bstack11l11111l1_opy_.bstack111l111l1ll_opy_(
                scenario, feature, request.node,
                name=bstack111l1l1ll11_opy_(request.node, scenario),
                started_at=bstack11l1ll11ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1l1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ῾"),
                tags=bstack111l1ll11l1_opy_(feature, scenario),
                bstack11l111llll_opy_=bstack1l1lll1lll_opy_.bstack11l111ll1l_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11l11l_opy_[request.node.nodeid][bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ῿")] = bstack11l111l1ll_opy_
            bstack11111ll1l11_opy_(bstack11l111l1ll_opy_.uuid)
            bstack1l1lll1lll_opy_.bstack11l11l11l1_opy_(bstack1ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ "), bstack11l111l1ll_opy_)
        except Exception as err:
            print(bstack1ll1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ "), str(err))
def bstack1111l111lll_opy_(bstack111lllll1l_opy_):
    if bstack111lllll1l_opy_ in store[bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ ")]:
        store[bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ ")].remove(bstack111lllll1l_opy_)
def bstack11111ll1l11_opy_(test_uuid):
    store[bstack1ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1lll1lll_opy_.bstack1111ll1ll1l_opy_
def bstack1111l11l11l_opy_(item, call, report):
    logger.debug(bstack1ll1l1_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩ "))
    global bstack11111lll1l1_opy_
    bstack11l11l11_opy_ = bstack11l1ll11ll_opy_()
    if hasattr(report, bstack1ll1l1_opy_ (u"ࠨࡵࡷࡳࡵ࠭ ")):
        bstack11l11l11_opy_ = bstack11l1l1l1l11_opy_(report.stop)
    elif hasattr(report, bstack1ll1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ ")):
        bstack11l11l11_opy_ = bstack11l1l1l1l11_opy_(report.start)
    try:
        if getattr(report, bstack1ll1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ "), bstack1ll1l1_opy_ (u"ࠫࠬ ")) == bstack1ll1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ "):
            logger.debug(bstack1ll1l1_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ​").format(getattr(report, bstack1ll1l1_opy_ (u"ࠧࡸࡪࡨࡲࠬ‌"), bstack1ll1l1_opy_ (u"ࠨࠩ‍")).__str__(), bstack11111lll1l1_opy_))
            if bstack11111lll1l1_opy_ == bstack1ll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ‎"):
                _111l11l11l_opy_[item.nodeid][bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ‏")] = bstack11l11l11_opy_
                bstack11111llll11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭‐"), report, call)
                store[bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ‑")] = None
            elif bstack11111lll1l1_opy_ == bstack1ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ‒"):
                bstack11l111l1ll_opy_ = _111l11l11l_opy_[item.nodeid][bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ–")]
                bstack11l111l1ll_opy_.set(hooks=_111l11l11l_opy_[item.nodeid].get(bstack1ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ—"), []))
                exception, bstack11l1111lll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1111lll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1l1_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ―"), bstack1ll1l1_opy_ (u"ࠪࠫ‖"))]
                bstack11l111l1ll_opy_.stop(time=bstack11l11l11_opy_, result=Result(result=getattr(report, bstack1ll1l1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ‗"), bstack1ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ‘")), exception=exception, bstack11l1111lll_opy_=bstack11l1111lll_opy_))
                bstack1l1lll1lll_opy_.bstack11l11l11l1_opy_(bstack1ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ’"), _111l11l11l_opy_[item.nodeid][bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ‚")])
        elif getattr(report, bstack1ll1l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭‛"), bstack1ll1l1_opy_ (u"ࠩࠪ“")) in [bstack1ll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ”"), bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭„")]:
            logger.debug(bstack1ll1l1_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ‟").format(getattr(report, bstack1ll1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ†"), bstack1ll1l1_opy_ (u"ࠧࠨ‡")).__str__(), bstack11111lll1l1_opy_))
            bstack11l111l11l_opy_ = item.nodeid + bstack1ll1l1_opy_ (u"ࠨ࠯ࠪ•") + getattr(report, bstack1ll1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ‣"), bstack1ll1l1_opy_ (u"ࠪࠫ․"))
            if getattr(report, bstack1ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ‥"), False):
                hook_type = bstack1ll1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ…") if getattr(report, bstack1ll1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ‧"), bstack1ll1l1_opy_ (u"ࠧࠨ ")) == bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ ") else bstack1ll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭‪")
                _111l11l11l_opy_[bstack11l111l11l_opy_] = {
                    bstack1ll1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ‫"): uuid4().__str__(),
                    bstack1ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ‬"): bstack11l11l11_opy_,
                    bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ‭"): hook_type
                }
            _111l11l11l_opy_[bstack11l111l11l_opy_][bstack1ll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ‮")] = bstack11l11l11_opy_
            bstack1111l111lll_opy_(_111l11l11l_opy_[bstack11l111l11l_opy_][bstack1ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ ")])
            bstack11111ll1ll1_opy_(item, _111l11l11l_opy_[bstack11l111l11l_opy_], bstack1ll1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ‰"), report, call)
            if getattr(report, bstack1ll1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ‱"), bstack1ll1l1_opy_ (u"ࠪࠫ′")) == bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ″"):
                if getattr(report, bstack1ll1l1_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭‴"), bstack1ll1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭‵")) == bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ‶"):
                    bstack111l1lll1l_opy_ = {
                        bstack1ll1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭‷"): uuid4().__str__(),
                        bstack1ll1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭‸"): bstack11l1ll11ll_opy_(),
                        bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ‹"): bstack11l1ll11ll_opy_()
                    }
                    _111l11l11l_opy_[item.nodeid] = {**_111l11l11l_opy_[item.nodeid], **bstack111l1lll1l_opy_}
                    bstack11111llll11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ›"))
                    bstack11111llll11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack1ll1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ※"), report, call)
    except Exception as err:
        print(bstack1ll1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ‼"), str(err))
def bstack11111ll1l1l_opy_(test, bstack111l1lll1l_opy_, result=None, call=None, bstack1lllllll11_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l111l1ll_opy_ = {
        bstack1ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ‽"): bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭‾")],
        bstack1ll1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ‿"): bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࠨ⁀"),
        bstack1ll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⁁"): test.name,
        bstack1ll1l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⁂"): {
            bstack1ll1l1_opy_ (u"࠭࡬ࡢࡰࡪࠫ⁃"): bstack1ll1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⁄"),
            bstack1ll1l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭⁅"): inspect.getsource(test.obj)
        },
        bstack1ll1l1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⁆"): test.name,
        bstack1ll1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⁇"): test.name,
        bstack1ll1l1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⁈"): bstack11l1ll1ll_opy_.bstack111l1l1l1l_opy_(test),
        bstack1ll1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⁉"): file_path,
        bstack1ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⁊"): file_path,
        bstack1ll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁋"): bstack1ll1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⁌"),
        bstack1ll1l1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⁍"): file_path,
        bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⁎"): bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁏")],
        bstack1ll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⁐"): bstack1ll1l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⁑"),
        bstack1ll1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⁒"): {
            bstack1ll1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⁓"): test.nodeid
        },
        bstack1ll1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⁔"): bstack11l1l111111_opy_(test.own_markers)
    }
    if bstack1lllllll11_opy_ in [bstack1ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⁕"), bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⁖")]:
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠬࡳࡥࡵࡣࠪ⁗")] = {
            bstack1ll1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⁘"): bstack111l1lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⁙"), [])
        }
    if bstack1lllllll11_opy_ == bstack1ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⁚"):
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⁛")] = bstack1ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⁜")
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⁝")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁞")]
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ ")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⁠")]
    if result:
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⁡")] = result.outcome
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⁢")] = result.duration * 1000
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁣")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁤")]
        if result.failed:
            bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⁥")] = bstack1l1lll1lll_opy_.bstack1111ll1l11_opy_(call.excinfo.typename)
            bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⁦")] = bstack1l1lll1lll_opy_.bstack1111ll111l1_opy_(call.excinfo, result)
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⁧")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⁨")]
    if outcome:
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⁩")] = bstack11l1llll1ll_opy_(outcome)
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⁪")] = 0
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁫")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⁬")]
        if bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⁭")] == bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⁮"):
            bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⁯")] = bstack1ll1l1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⁰")  # bstack1111l1l1111_opy_
            bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫⁱ")] = [{bstack1ll1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⁲"): [bstack1ll1l1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⁳")]}]
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⁴")] = bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⁵")]
    return bstack11l111l1ll_opy_
def bstack1111l11ll11_opy_(test, bstack111lll1l11_opy_, bstack1lllllll11_opy_, result, call, outcome, bstack1111l111ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⁶")]
    hook_name = bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⁷")]
    hook_data = {
        bstack1ll1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⁸"): bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⁹")],
        bstack1ll1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ⁺"): bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⁻"),
        bstack1ll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⁼"): bstack1ll1l1_opy_ (u"ࠨࡽࢀࠫ⁽").format(bstack111l1ll1111_opy_(hook_name)),
        bstack1ll1l1_opy_ (u"ࠩࡥࡳࡩࡿࠧ⁾"): {
            bstack1ll1l1_opy_ (u"ࠪࡰࡦࡴࡧࠨⁿ"): bstack1ll1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ₀"),
            bstack1ll1l1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ₁"): None
        },
        bstack1ll1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ₂"): test.name,
        bstack1ll1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ₃"): bstack11l1ll1ll_opy_.bstack111l1l1l1l_opy_(test, hook_name),
        bstack1ll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ₄"): file_path,
        bstack1ll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ₅"): file_path,
        bstack1ll1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₆"): bstack1ll1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ₇"),
        bstack1ll1l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ₈"): file_path,
        bstack1ll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ₉"): bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ₊")],
        bstack1ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ₋"): bstack1ll1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ₌") if bstack11111lll1l1_opy_ == bstack1ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ₍") else bstack1ll1l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ₎"),
        bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ₏"): hook_type
    }
    bstack111l111ll11_opy_ = bstack111lll1l1l_opy_(_111l11l11l_opy_.get(test.nodeid, None))
    if bstack111l111ll11_opy_:
        hook_data[bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫₐ")] = bstack111l111ll11_opy_
    if result:
        hook_data[bstack1ll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧₑ")] = result.outcome
        hook_data[bstack1ll1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩₒ")] = result.duration * 1000
        hook_data[bstack1ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧₓ")] = bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨₔ")]
        if result.failed:
            hook_data[bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪₕ")] = bstack1l1lll1lll_opy_.bstack1111ll1l11_opy_(call.excinfo.typename)
            hook_data[bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ₖ")] = bstack1l1lll1lll_opy_.bstack1111ll111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ₗ")] = bstack11l1llll1ll_opy_(outcome)
        hook_data[bstack1ll1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨₘ")] = 100
        hook_data[bstack1ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ₙ")] = bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧₚ")]
        if hook_data[bstack1ll1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪₛ")] == bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫₜ"):
            hook_data[bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ₝")] = bstack1ll1l1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ₞")  # bstack1111l1l1111_opy_
            hook_data[bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ₟")] = [{bstack1ll1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ₠"): [bstack1ll1l1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭₡")]}]
    if bstack1111l111ll1_opy_:
        hook_data[bstack1ll1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₢")] = bstack1111l111ll1_opy_.result
        hook_data[bstack1ll1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ₣")] = bstack11l1ll11lll_opy_(bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₤")], bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ₥")])
        hook_data[bstack1ll1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₦")] = bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₧")]
        if hook_data[bstack1ll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ₨")] == bstack1ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ₩"):
            hook_data[bstack1ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ₪")] = bstack1l1lll1lll_opy_.bstack1111ll1l11_opy_(bstack1111l111ll1_opy_.exception_type)
            hook_data[bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭₫")] = [{bstack1ll1l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ€"): bstack11ll1111l1l_opy_(bstack1111l111ll1_opy_.exception)}]
    return hook_data
def bstack11111llll11_opy_(test, bstack111l1lll1l_opy_, bstack1lllllll11_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1ll1l1_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ₭").format(bstack1lllllll11_opy_))
    bstack11l111l1ll_opy_ = bstack11111ll1l1l_opy_(test, bstack111l1lll1l_opy_, result, call, bstack1lllllll11_opy_, outcome)
    driver = getattr(test, bstack1ll1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ₮"), None)
    if bstack1lllllll11_opy_ == bstack1ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ₯") and driver:
        bstack11l111l1ll_opy_[bstack1ll1l1_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ₰")] = bstack1l1lll1lll_opy_.bstack11l111ll1l_opy_(driver)
    if bstack1lllllll11_opy_ == bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ₱"):
        bstack1lllllll11_opy_ = bstack1ll1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ₲")
    bstack111ll1l1ll_opy_ = {
        bstack1ll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ₳"): bstack1lllllll11_opy_,
        bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ₴"): bstack11l111l1ll_opy_
    }
    bstack1l1lll1lll_opy_.bstack1l111l1ll_opy_(bstack111ll1l1ll_opy_)
    if bstack1lllllll11_opy_ == bstack1ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ₵"):
        threading.current_thread().bstackTestMeta = {bstack1ll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ₶"): bstack1ll1l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ₷")}
    elif bstack1lllllll11_opy_ == bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭₸"):
        threading.current_thread().bstackTestMeta = {bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ₹"): getattr(result, bstack1ll1l1_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ₺"), bstack1ll1l1_opy_ (u"ࠧࠨ₻"))}
def bstack11111ll1ll1_opy_(test, bstack111l1lll1l_opy_, bstack1lllllll11_opy_, result=None, call=None, outcome=None, bstack1111l111ll1_opy_=None):
    logger.debug(bstack1ll1l1_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ₼").format(bstack1lllllll11_opy_))
    hook_data = bstack1111l11ll11_opy_(test, bstack111l1lll1l_opy_, bstack1lllllll11_opy_, result, call, outcome, bstack1111l111ll1_opy_)
    bstack111ll1l1ll_opy_ = {
        bstack1ll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭₽"): bstack1lllllll11_opy_,
        bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ₾"): hook_data
    }
    bstack1l1lll1lll_opy_.bstack1l111l1ll_opy_(bstack111ll1l1ll_opy_)
def bstack111lll1l1l_opy_(bstack111l1lll1l_opy_):
    if not bstack111l1lll1l_opy_:
        return None
    if bstack111l1lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ₿"), None):
        return getattr(bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⃀")], bstack1ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⃁"), None)
    return bstack111l1lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⃂"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.LOG, bstack1lll1l11l1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_.LOG, bstack1lll1l11l1l_opy_.POST, request, caplog)
        return # skip all existing bstack11111llllll_opy_
    try:
        if not bstack1l1lll1lll_opy_.on():
            return
        places = [bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⃃"), bstack1ll1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧ⃄"), bstack1ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⃅")]
        logs = []
        for bstack11111lll11l_opy_ in places:
            records = caplog.get_records(bstack11111lll11l_opy_)
            bstack1111l11l1l1_opy_ = bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃆") if bstack11111lll11l_opy_ == bstack1ll1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⃇") else bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃈")
            bstack11111lll111_opy_ = request.node.nodeid + (bstack1ll1l1_opy_ (u"ࠧࠨ⃉") if bstack11111lll11l_opy_ == bstack1ll1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭⃊") else bstack1ll1l1_opy_ (u"ࠩ࠰ࠫ⃋") + bstack11111lll11l_opy_)
            test_uuid = bstack111lll1l1l_opy_(_111l11l11l_opy_.get(bstack11111lll111_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1l11ll1l_opy_(record.message):
                    continue
                logs.append({
                    bstack1ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⃌"): bstack11l1l1l1ll1_opy_(record.created).isoformat() + bstack1ll1l1_opy_ (u"ࠫ࡟࠭⃍"),
                    bstack1ll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⃎"): record.levelname,
                    bstack1ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⃏"): record.message,
                    bstack1111l11l1l1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1lll1lll_opy_.bstack1l111lll1_opy_(logs)
    except Exception as err:
        print(bstack1ll1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ⃐"), str(err))
def bstack11l11lll1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11111l1l1_opy_
    bstack111ll111_opy_ = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ⃑"), None) and bstack11111l111_opy_(
            threading.current_thread(), bstack1ll1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⃒"), None)
    bstack1lllll1lll_opy_ = getattr(driver, bstack1ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰ⃓ࠪ"), None) != None and getattr(driver, bstack1ll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⃔"), None) == True
    if sequence == bstack1ll1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⃕") and driver != None:
      if not bstack11111l1l1_opy_ and bstack1l1llll11ll_opy_() and bstack1ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃖") in CONFIG and CONFIG[bstack1ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃗")] == True and bstack1ll1l11l1l_opy_.bstack1ll1lll11l_opy_(driver_command) and (bstack1lllll1lll_opy_ or bstack111ll111_opy_) and not bstack1lllll1l11_opy_(args):
        try:
          bstack11111l1l1_opy_ = True
          logger.debug(bstack1ll1l1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿ⃘ࠪ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃ⃙ࠧ").format(str(err)))
        bstack11111l1l1_opy_ = False
    if sequence == bstack1ll1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳ⃚ࠩ"):
        if driver_command == bstack1ll1l1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ⃛"):
            bstack1l1lll1lll_opy_.bstack1ll1111l11_opy_({
                bstack1ll1l1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⃜"): response[bstack1ll1l1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ⃝")],
                bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃞"): store[bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⃟")]
            })
def bstack1ll1l111l1_opy_():
    global bstack1l1ll1ll11_opy_
    bstack1l1ll1111l_opy_.bstack1lll111lll_opy_()
    logging.shutdown()
    bstack1l1lll1lll_opy_.bstack111ll11l11_opy_()
    for driver in bstack1l1ll1ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111l11111l_opy_(*args):
    global bstack1l1ll1ll11_opy_
    bstack1l1lll1lll_opy_.bstack111ll11l11_opy_()
    for driver in bstack1l1ll1ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1lllll_opy_, stage=STAGE.bstack1llll1l1_opy_, bstack1l1l111l1_opy_=bstack1l1111l111_opy_)
def bstack11111111_opy_(self, *args, **kwargs):
    bstack11ll1ll1_opy_ = bstack1lll111l1_opy_(self, *args, **kwargs)
    bstack1llll1ll1l_opy_ = getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⃠"), None)
    if bstack1llll1ll1l_opy_ and bstack1llll1ll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⃡"), bstack1ll1l1_opy_ (u"ࠫࠬ⃢")) == bstack1ll1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⃣"):
        bstack1l1lll1lll_opy_.bstack11ll11lll_opy_(self)
    return bstack11ll1ll1_opy_
@measure(event_name=EVENTS.bstack1ll1lll1_opy_, stage=STAGE.bstack1l11ll11_opy_, bstack1l1l111l1_opy_=bstack1l1111l111_opy_)
def bstack1llll1llll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
    if bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⃤")):
        return
    bstack11ll11ll_opy_.bstack1ll11111_opy_(bstack1ll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧ⃥ࠫ"), True)
    global bstack1l111l1l1l_opy_
    global bstack111ll11l1_opy_
    bstack1l111l1l1l_opy_ = framework_name
    logger.info(bstack11l11ll11l_opy_.format(bstack1l111l1l1l_opy_.split(bstack1ll1l1_opy_ (u"ࠨ࠯⃦ࠪ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1llll11ll_opy_():
            Service.start = bstack1111lll1l_opy_
            Service.stop = bstack1ll11ll1l_opy_
            webdriver.Remote.get = bstack1l1l1l111l_opy_
            webdriver.Remote.__init__ = bstack1lll111ll1_opy_
            if not isinstance(os.getenv(bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ⃧")), str):
                return
            WebDriver.close = bstack1llll1111_opy_
            WebDriver.quit = bstack11llll1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1lll1lll_opy_.on():
            webdriver.Remote.__init__ = bstack11111111_opy_
        bstack111ll11l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1ll1l1_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⃨")):
        bstack111ll11l1_opy_ = eval(os.environ.get(bstack1ll1l1_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⃩")))
    if not bstack111ll11l1_opy_:
        bstack11llll11l1_opy_(bstack1ll1l1_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪ⃪ࠢ"), bstack11lll111_opy_)
    if bstack1111l1l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1ll1l1ll11_opy_ = bstack11ll11l1l1_opy_
        except Exception as e:
            logger.error(bstack11lll111ll_opy_.format(str(e)))
    if bstack1ll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ⃫࠭") in str(framework_name).lower():
        if not bstack1l1llll11ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1l1lll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1l111l1_opy_
            Config.getoption = bstack1lll1lll1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1111ll11_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1ll111_opy_, stage=STAGE.bstack1llll1l1_opy_, bstack1l1l111l1_opy_=bstack1l1111l111_opy_)
def bstack11llll1l1_opy_(self):
    global bstack1l111l1l1l_opy_
    global bstack111lll1l1_opy_
    global bstack1l1llll11_opy_
    try:
        if bstack1ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ⃬ࠧ") in bstack1l111l1l1l_opy_ and self.session_id != None and bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷ⃭ࠬ"), bstack1ll1l1_opy_ (u"⃮ࠩࠪ")) != bstack1ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧ⃯ࠫ"):
            bstack11ll1ll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⃰") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⃱")
            bstack1ll1lll11_opy_(logger, True)
            if self != None:
                bstack111l1l1l_opy_(self, bstack11ll1ll1l1_opy_, bstack1ll1l1_opy_ (u"࠭ࠬࠡࠩ⃲").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lllll11l11_opy_(bstack1lll1111l11_opy_):
            item = store.get(bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⃳"), None)
            if item is not None and bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⃴"), None):
                bstack1111l111_opy_.bstack1ll1l11lll_opy_(self, bstack111lll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1l1_opy_ (u"ࠩࠪ⃵")
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ⃶") + str(e))
    bstack1l1llll11_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1llll1l1_opy_, bstack1l1l111l1_opy_=bstack1l1111l111_opy_)
def bstack1lll111ll1_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll11ll11l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack111lll1l1_opy_
    global bstack1l1111l111_opy_
    global bstack1ll1l11l_opy_
    global bstack1l111l1l1l_opy_
    global bstack1lll111l1_opy_
    global bstack1l1ll1ll11_opy_
    global bstack1l11ll1ll1_opy_
    global bstack11lll11l_opy_
    global bstack111lll1l_opy_
    CONFIG[bstack1ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⃷")] = str(bstack1l111l1l1l_opy_) + str(__version__)
    command_executor = bstack1llllll1ll_opy_(bstack1l11ll1ll1_opy_, CONFIG)
    logger.debug(bstack11lll11l11_opy_.format(command_executor))
    proxy = bstack11lll11lll_opy_(CONFIG, proxy)
    bstack1lll1l111_opy_ = 0
    try:
        if bstack1ll1l11l_opy_ is True:
            bstack1lll1l111_opy_ = int(os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⃸")))
    except:
        bstack1lll1l111_opy_ = 0
    bstack11l111l11_opy_ = bstack1l1l1l11l1_opy_(CONFIG, bstack1lll1l111_opy_)
    logger.debug(bstack11ll1l1lll_opy_.format(str(bstack11l111l11_opy_)))
    bstack111lll1l_opy_ = CONFIG.get(bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⃹"))[bstack1lll1l111_opy_]
    if bstack1ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⃺") in CONFIG and CONFIG[bstack1ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⃻")]:
        bstack1l111ll1_opy_(bstack11l111l11_opy_, bstack11lll11l_opy_)
    if bstack1l11llll_opy_.bstack111111ll1_opy_(CONFIG, bstack1lll1l111_opy_) and bstack1l11llll_opy_.bstack1l11ll1l11_opy_(bstack11l111l11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lllll11l11_opy_(bstack1lll1111l11_opy_):
            bstack1l11llll_opy_.set_capabilities(bstack11l111l11_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll111111l_opy_ = bstack11l1111ll_opy_(desired_capabilities)
        bstack1ll111111l_opy_[bstack1ll1l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⃼")] = bstack1l11111lll_opy_(CONFIG)
        bstack1l1111l1ll_opy_ = bstack1l1l1l11l1_opy_(bstack1ll111111l_opy_)
        if bstack1l1111l1ll_opy_:
            bstack11l111l11_opy_ = update(bstack1l1111l1ll_opy_, bstack11l111l11_opy_)
        desired_capabilities = None
    if options:
        bstack1ll11ll1ll_opy_(options, bstack11l111l11_opy_)
    if not options:
        options = bstack1l111ll111_opy_(bstack11l111l11_opy_)
    if proxy and bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⃽")):
        options.proxy(proxy)
    if options and bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⃾")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11ll1llll1_opy_() < version.parse(bstack1ll1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⃿")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l111l11_opy_)
    logger.info(bstack1111l11ll_opy_)
    bstack1l111l1111_opy_.end(EVENTS.bstack1ll1lll1_opy_.value, EVENTS.bstack1ll1lll1_opy_.value + bstack1ll1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ℀"),
                               EVENTS.bstack1ll1lll1_opy_.value + bstack1ll1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ℁"), True, None)
    if bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨℂ")):
        bstack1lll111l1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ℃")):
        bstack1lll111l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1ll11ll11l_opy_=bstack1ll11ll11l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ℄")):
        bstack1lll111l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll11ll11l_opy_=bstack1ll11ll11l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll111l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll11ll11l_opy_=bstack1ll11ll11l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l11l1111_opy_ = bstack1ll1l1_opy_ (u"ࠫࠬ℅")
        if bstack11ll1llll1_opy_() >= version.parse(bstack1ll1l1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭℆")):
            bstack1l11l1111_opy_ = self.caps.get(bstack1ll1l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨℇ"))
        else:
            bstack1l11l1111_opy_ = self.capabilities.get(bstack1ll1l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ℈"))
        if bstack1l11l1111_opy_:
            bstack11l1l1l11l_opy_(bstack1l11l1111_opy_)
            if bstack11ll1llll1_opy_() <= version.parse(bstack1ll1l1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ℉")):
                self.command_executor._url = bstack1ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥℊ") + bstack1l11ll1ll1_opy_ + bstack1ll1l1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢℋ")
            else:
                self.command_executor._url = bstack1ll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨℌ") + bstack1l11l1111_opy_ + bstack1ll1l1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨℍ")
            logger.debug(bstack1ll1l1l1_opy_.format(bstack1l11l1111_opy_))
        else:
            logger.debug(bstack1l1l1lll1_opy_.format(bstack1ll1l1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢℎ")))
    except Exception as e:
        logger.debug(bstack1l1l1lll1_opy_.format(e))
    bstack111lll1l1_opy_ = self.session_id
    if bstack1ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧℏ") in bstack1l111l1l1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬℐ"), None)
        if item:
            bstack11111ll11ll_opy_ = getattr(item, bstack1ll1l1_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧℑ"), False)
            if not getattr(item, bstack1ll1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫℒ"), None) and bstack11111ll11ll_opy_:
                setattr(store[bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨℓ")], bstack1ll1l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭℔"), self)
        bstack1llll1ll1l_opy_ = getattr(threading.current_thread(), bstack1ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧℕ"), None)
        if bstack1llll1ll1l_opy_ and bstack1llll1ll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ№"), bstack1ll1l1_opy_ (u"ࠨࠩ℗")) == bstack1ll1l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ℘"):
            bstack1l1lll1lll_opy_.bstack11ll11lll_opy_(self)
    bstack1l1ll1ll11_opy_.append(self)
    if bstack1ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ℙ") in CONFIG and bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩℚ") in CONFIG[bstack1ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨℛ")][bstack1lll1l111_opy_]:
        bstack1l1111l111_opy_ = CONFIG[bstack1ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩℜ")][bstack1lll1l111_opy_][bstack1ll1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬℝ")]
    logger.debug(bstack11111lll1_opy_.format(bstack111lll1l1_opy_))
@measure(event_name=EVENTS.bstack1ll11ll1_opy_, stage=STAGE.bstack1llll1l1_opy_, bstack1l1l111l1_opy_=bstack1l1111l111_opy_)
def bstack1l1l1l111l_opy_(self, url):
    global bstack11lll1ll11_opy_
    global CONFIG
    try:
        bstack111ll111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l11111111_opy_.format(str(err)))
    try:
        bstack11lll1ll11_opy_(self, url)
    except Exception as e:
        try:
            bstack11l1l111ll_opy_ = str(e)
            if any(err_msg in bstack11l1l111ll_opy_ for err_msg in bstack1l111l11ll_opy_):
                bstack111ll111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l11111111_opy_.format(str(err)))
        raise e
def bstack111llll1_opy_(item, when):
    global bstack1llll1l1l_opy_
    try:
        bstack1llll1l1l_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1111ll11_opy_(item, call, rep):
    global bstack1l1l1l1ll_opy_
    global bstack1l1ll1ll11_opy_
    name = bstack1ll1l1_opy_ (u"ࠨࠩ℞")
    try:
        if rep.when == bstack1ll1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧ℟"):
            bstack111lll1l1_opy_ = threading.current_thread().bstackSessionId
            bstack11111lll1ll_opy_ = item.config.getoption(bstack1ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ℠"))
            try:
                if (str(bstack11111lll1ll_opy_).lower() != bstack1ll1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩ℡")):
                    name = str(rep.nodeid)
                    bstack1l1l11111_opy_ = bstack11ll1ll111_opy_(bstack1ll1l1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭™"), name, bstack1ll1l1_opy_ (u"࠭ࠧ℣"), bstack1ll1l1_opy_ (u"ࠧࠨℤ"), bstack1ll1l1_opy_ (u"ࠨࠩ℥"), bstack1ll1l1_opy_ (u"ࠩࠪΩ"))
                    os.environ[bstack1ll1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭℧")] = name
                    for driver in bstack1l1ll1ll11_opy_:
                        if bstack111lll1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l11111_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫℨ").format(str(e)))
            try:
                bstack1ll1llll1l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭℩"):
                    status = bstack1ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭K") if rep.outcome.lower() == bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧÅ") else bstack1ll1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨℬ")
                    reason = bstack1ll1l1_opy_ (u"ࠩࠪℭ")
                    if status == bstack1ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ℮"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩℯ") if status == bstack1ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬℰ") else bstack1ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬℱ")
                    data = name + bstack1ll1l1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩℲ") if status == bstack1ll1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨℳ") else name + bstack1ll1l1_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬℴ") + reason
                    bstack111lll111_opy_ = bstack11ll1ll111_opy_(bstack1ll1l1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬℵ"), bstack1ll1l1_opy_ (u"ࠫࠬℶ"), bstack1ll1l1_opy_ (u"ࠬ࠭ℷ"), bstack1ll1l1_opy_ (u"࠭ࠧℸ"), level, data)
                    for driver in bstack1l1ll1ll11_opy_:
                        if bstack111lll1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack111lll111_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫℹ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ℺").format(str(e)))
    bstack1l1l1l1ll_opy_(item, call, rep)
notset = Notset()
def bstack1lll1lll1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11lllll1_opy_
    if str(name).lower() == bstack1ll1l1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ℻"):
        return bstack1ll1l1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤℼ")
    else:
        return bstack11lllll1_opy_(self, name, default, skip)
def bstack11ll11l1l1_opy_(self):
    global CONFIG
    global bstack1lll1l1lll_opy_
    try:
        proxy = bstack11ll11l1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1l1_opy_ (u"ࠫ࠳ࡶࡡࡤࠩℽ")):
                proxies = bstack1l1111l1l_opy_(proxy, bstack1llllll1ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack11l11lll1_opy_ = proxies.popitem()
                    if bstack1ll1l1_opy_ (u"ࠧࡀ࠯࠰ࠤℾ") in bstack11l11lll1_opy_:
                        return bstack11l11lll1_opy_
                    else:
                        return bstack1ll1l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢℿ") + bstack11l11lll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ⅀").format(str(e)))
    return bstack1lll1l1lll_opy_(self)
def bstack1111l1l1l_opy_():
    return (bstack1ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⅁") in CONFIG or bstack1ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⅂") in CONFIG) and bstack11llllll_opy_() and bstack11ll1llll1_opy_() >= version.parse(
        bstack1111lll11_opy_)
def bstack1l1llll1l1_opy_(self,
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
    global bstack1l1111l111_opy_
    global bstack1ll1l11l_opy_
    global bstack1l111l1l1l_opy_
    CONFIG[bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⅃")] = str(bstack1l111l1l1l_opy_) + str(__version__)
    bstack1lll1l111_opy_ = 0
    try:
        if bstack1ll1l11l_opy_ is True:
            bstack1lll1l111_opy_ = int(os.environ.get(bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⅄")))
    except:
        bstack1lll1l111_opy_ = 0
    CONFIG[bstack1ll1l1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦⅅ")] = True
    bstack11l111l11_opy_ = bstack1l1l1l11l1_opy_(CONFIG, bstack1lll1l111_opy_)
    logger.debug(bstack11ll1l1lll_opy_.format(str(bstack11l111l11_opy_)))
    if CONFIG.get(bstack1ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪⅆ")):
        bstack1l111ll1_opy_(bstack11l111l11_opy_, bstack11lll11l_opy_)
    if bstack1ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅇ") in CONFIG and bstack1ll1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ⅈ") in CONFIG[bstack1ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬⅉ")][bstack1lll1l111_opy_]:
        bstack1l1111l111_opy_ = CONFIG[bstack1ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⅊")][bstack1lll1l111_opy_][bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⅋")]
    import urllib
    import json
    if bstack1ll1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⅌") in CONFIG and str(CONFIG[bstack1ll1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⅍")]).lower() != bstack1ll1l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ⅎ"):
        bstack111l111l1_opy_ = bstack11ll11111l_opy_()
        bstack11l1l11l11_opy_ = bstack111l111l1_opy_ + urllib.parse.quote(json.dumps(bstack11l111l11_opy_))
    else:
        bstack11l1l11l11_opy_ = bstack1ll1l1_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ⅏") + urllib.parse.quote(json.dumps(bstack11l111l11_opy_))
    browser = self.connect(bstack11l1l11l11_opy_)
    return browser
def bstack11l11llll_opy_():
    global bstack111ll11l1_opy_
    global bstack1l111l1l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1ll11l1l_opy_
        if not bstack1l1llll11ll_opy_():
            global bstack1ll1l1l1ll_opy_
            if not bstack1ll1l1l1ll_opy_:
                from bstack_utils.helper import bstack1ll1l1111l_opy_, bstack1lll1lll_opy_
                bstack1ll1l1l1ll_opy_ = bstack1ll1l1111l_opy_()
                bstack1lll1lll_opy_(bstack1l111l1l1l_opy_)
            BrowserType.connect = bstack1l1ll11l1l_opy_
            return
        BrowserType.launch = bstack1l1llll1l1_opy_
        bstack111ll11l1_opy_ = True
    except Exception as e:
        pass
def bstack1111l11lll1_opy_():
    global CONFIG
    global bstack1l1111lll1_opy_
    global bstack1l11ll1ll1_opy_
    global bstack11lll11l_opy_
    global bstack1ll1l11l_opy_
    global bstack1l1111l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ⅐")))
    bstack1l1111lll1_opy_ = eval(os.environ.get(bstack1ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⅑")))
    bstack1l11ll1ll1_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ⅒"))
    bstack1l11llll11_opy_(CONFIG, bstack1l1111lll1_opy_)
    bstack1l1111l1l1_opy_ = bstack1l1ll1111l_opy_.bstack1l1l1l111_opy_(CONFIG, bstack1l1111l1l1_opy_)
    if cli.bstack1ll1l1111_opy_():
        bstack1111111l_opy_.invoke(bstack1l1111ll1l_opy_.CONNECT, bstack11111111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⅓"), bstack1ll1l1_opy_ (u"࠭࠰ࠨ⅔")))
        cli.bstack1lll1111ll1_opy_(cli_context.platform_index)
        cli.bstack1lll1l1l1ll_opy_(bstack1llllll1ll_opy_(bstack1l11ll1ll1_opy_, CONFIG), cli_context.platform_index, bstack1l111ll111_opy_)
        cli.bstack1llll11111l_opy_()
        logger.debug(bstack1ll1l1_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⅕") + str(cli_context.platform_index) + bstack1ll1l1_opy_ (u"ࠣࠤ⅖"))
        return # skip all existing bstack11111llllll_opy_
    global bstack1lll111l1_opy_
    global bstack1l1llll11_opy_
    global bstack111lllll1_opy_
    global bstack1l111llll_opy_
    global bstack11l1l1ll_opy_
    global bstack1l1ll1ll1_opy_
    global bstack11l111ll1_opy_
    global bstack11lll1ll11_opy_
    global bstack1lll1l1lll_opy_
    global bstack11lllll1_opy_
    global bstack1llll1l1l_opy_
    global bstack1l1l1l1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll111l1_opy_ = webdriver.Remote.__init__
        bstack1l1llll11_opy_ = WebDriver.quit
        bstack11l111ll1_opy_ = WebDriver.close
        bstack11lll1ll11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⅗") in CONFIG or bstack1ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⅘") in CONFIG) and bstack11llllll_opy_():
        if bstack11ll1llll1_opy_() < version.parse(bstack1111lll11_opy_):
            logger.error(bstack11l1l111l_opy_.format(bstack11ll1llll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1lll1l1lll_opy_ = RemoteConnection._1ll1l1ll11_opy_
            except Exception as e:
                logger.error(bstack11lll111ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11lllll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1llll1l1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11ll1111ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1l1l1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ⅙"))
    bstack11lll11l_opy_ = CONFIG.get(bstack1ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⅚"), {}).get(bstack1ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⅛"))
    bstack1ll1l11l_opy_ = True
    bstack1llll1llll_opy_(bstack1l1111l1_opy_)
if (bstack11ll11l1l11_opy_()):
    bstack1111l11lll1_opy_()
@bstack111ll11ll1_opy_(class_method=False)
def bstack11111ll11l1_opy_(hook_name, event, bstack1l11lllll1l_opy_=None):
    if hook_name not in [bstack1ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⅜"), bstack1ll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⅝"), bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⅞"), bstack1ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⅟"), bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩⅠ"), bstack1ll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ⅱ"), bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬⅢ"), bstack1ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩⅣ")]:
        return
    node = store[bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬⅤ")]
    if hook_name in [bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨⅥ"), bstack1ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬⅦ")]:
        node = store[bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪⅧ")]
    elif hook_name in [bstack1ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪⅨ"), bstack1ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧⅩ")]:
        node = store[bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬⅪ")]
    hook_type = bstack111l1l1lll1_opy_(hook_name)
    if event == bstack1ll1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨⅫ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_[hook_type], bstack1lll1l11l1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111lll1l11_opy_ = {
            bstack1ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧⅬ"): uuid,
            bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧⅭ"): bstack11l1ll11ll_opy_(),
            bstack1ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩⅮ"): bstack1ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪⅯ"),
            bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩⅰ"): hook_type,
            bstack1ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪⅱ"): hook_name
        }
        store[bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬⅲ")].append(uuid)
        bstack1111l111l1l_opy_ = node.nodeid
        if hook_type == bstack1ll1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧⅳ"):
            if not _111l11l11l_opy_.get(bstack1111l111l1l_opy_, None):
                _111l11l11l_opy_[bstack1111l111l1l_opy_] = {bstack1ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩⅴ"): []}
            _111l11l11l_opy_[bstack1111l111l1l_opy_][bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪⅵ")].append(bstack111lll1l11_opy_[bstack1ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪⅶ")])
        _111l11l11l_opy_[bstack1111l111l1l_opy_ + bstack1ll1l1_opy_ (u"࠭࠭ࠨⅷ") + hook_name] = bstack111lll1l11_opy_
        bstack11111ll1ll1_opy_(node, bstack111lll1l11_opy_, bstack1ll1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅸ"))
    elif event == bstack1ll1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧⅹ"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllllll1ll_opy_[hook_type], bstack1lll1l11l1l_opy_.POST, node, None, bstack1l11lllll1l_opy_)
            return
        bstack11l111l11l_opy_ = node.nodeid + bstack1ll1l1_opy_ (u"ࠩ࠰ࠫⅺ") + hook_name
        _111l11l11l_opy_[bstack11l111l11l_opy_][bstack1ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨⅻ")] = bstack11l1ll11ll_opy_()
        bstack1111l111lll_opy_(_111l11l11l_opy_[bstack11l111l11l_opy_][bstack1ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩⅼ")])
        bstack11111ll1ll1_opy_(node, _111l11l11l_opy_[bstack11l111l11l_opy_], bstack1ll1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧⅽ"), bstack1111l111ll1_opy_=bstack1l11lllll1l_opy_)
def bstack1111l111111_opy_():
    global bstack11111lll1l1_opy_
    if bstack111111111_opy_():
        bstack11111lll1l1_opy_ = bstack1ll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪⅾ")
    else:
        bstack11111lll1l1_opy_ = bstack1ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧⅿ")
@bstack1l1lll1lll_opy_.bstack1111ll1ll1l_opy_
def bstack1111l111l11_opy_():
    bstack1111l111111_opy_()
    if cli.is_running():
        try:
            bstack11l11ll1l1l_opy_(bstack11111ll11l1_opy_)
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤↀ").format(e))
        return
    if bstack11llllll_opy_():
        bstack11ll11ll_opy_ = Config.bstack1l11l1l1ll_opy_()
        bstack1ll1l1_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬↁ")
        if bstack11ll11ll_opy_.get_property(bstack1ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧↂ")):
            if CONFIG.get(bstack1ll1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫↃ")) is not None and int(CONFIG[bstack1ll1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬↄ")]) > 1:
                bstack11ll1l1l_opy_(bstack11l11lll1l_opy_)
            return
        bstack11ll1l1l_opy_(bstack11l11lll1l_opy_)
    try:
        bstack11l11ll1l1l_opy_(bstack11111ll11l1_opy_)
    except Exception as e:
        logger.debug(bstack1ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢↅ").format(e))
bstack1111l111l11_opy_()