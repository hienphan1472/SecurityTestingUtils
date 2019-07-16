from mitmproxy import proxy, options, ctx
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http


class AdjustBody:
    def response(self, flow: http.HTTPFlow) -> None:
        if "api/v5" in flow.request.url:
            print("Before intercept: %s" % flow.response.text)
            flow.response.content = bytes("This is replacement response", "UTF-8")
            print("After intercept: %s" % flow.response.text)


def start():
    myaddon = AdjustBody()
    opts = options.Options(listen_host='192.168.1.224', listen_port=8888, confdir="/Users/hienphan/.mitmproxy")
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)
    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()


start()
