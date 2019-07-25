import asyncio
from mitmproxy import proxy, options, ctx
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http


class AdjustBody:
    def response(self, flow: http.HTTPFlow) -> None:
        if "apiqa.vungle.com/api/v5/ads" in flow.request.url:
            print("Before intercept: %s" % flow.response.text)
            flow.response.content = bytes("This is replacement response", "UTF-8")
            print("After intercept: %s" % flow.response.text)
            asyncio.ensure_future(stop())


def start():
    add_on = AdjustBody()

    opts = options.Options(listen_host='192.168.1.224', listen_port=8888, confdir="/Users/hienphan/.mitmproxy")
    proxy_conf = proxy.config.ProxyConfig(opts)

    dump_master = DumpMaster(opts)
    dump_master.server = proxy.server.ProxyServer(proxy_conf)
    dump_master.addons.add(add_on)

    try:
        dump_master.run()
    except KeyboardInterrupt:
        dump_master.shutdown()


async def stop():
    await asyncio.sleep(5)
    print("shutting down...")
    ctx.master.shutdown()


