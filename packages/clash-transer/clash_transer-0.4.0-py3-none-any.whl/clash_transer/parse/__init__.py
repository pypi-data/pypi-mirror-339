import base64
from typing import Any, Dict, Iterator, Optional
from urllib.parse import ParseResult, urlparse

from ..log import LOGGER
from ..worker.vars import dist_file_v
from .protocol import parse_hysteria2, parse_ss, parse_ssr, parse_vless, parse_vmess


class Parse:
    @classmethod
    def parse(cls, text: str, suffix: str):
        return cls(text, suffix)

    @classmethod
    def parse_text(cls, text: str):
        return cls(text)

    def __init__(self, text: str, suffix: Optional[str] = None) -> None:
        self.server_ports = set()
        match suffix.lower():
            case "ssr":
                self.res = self.parse_ssr(text)
            case "ss":
                self.res = self.parse_ss(text)
            case "vmess":
                self.res = self.parse_vmess(text)
            case "list":
                self.res = self.parse_list(text)
            case _:
                self.res = self.parse_text_seprate_lines(text)

        LOGGER.info("解析完成 %s", dist_file_v.get().name)

    @staticmethod
    def b64decode(text):
        if isinstance(text, str):
            byte = text.encode("utf-8")
        else:
            byte = text
        if not byte.endswith(b"="):
            byte = byte + b"=" * (4 - (len(byte) % 4))
        res = base64.urlsafe_b64decode(byte)
        return res

    def parse_one_line_text(self, text: str):
        link: ParseResult = urlparse(text)
        return self.parse_one_line_text(link)

    def parse_one_link_obj(self, link: ParseResult) -> Optional[Dict[str, Any]]:
        match link.scheme:
            case "ss":
                return parse_ss(link)
            case "ssr":
                return parse_ssr(link)
            case "vless":
                return parse_vless(link)
            case "vmess":
                return parse_vmess(link)
            case "hysteria2":
                return parse_hysteria2(link)
            case _:
                return None

    def parse_text_seprate_lines(self, text):
        link_lines = self.b64decode(text).strip().splitlines()
        link_dicts: Iterator[Dict[str, Any]] = (
            self.parse_one_line_text(i) for i in link_lines if i
        )
        yield from link_dicts

    def parse_ssr(self, text):
        decoded_str = self.b64decode(text)
        links = decoded_str.splitlines()
        for link in links:
            link = link.decode("utf-8")
            parsed_url = urlparse(link)
            tmp = self.parse_one_link_obj(parsed_url)
            if tmp:
                yield tmp

    def parse_ss(self, text):
        decoded_str = self.b64decode(text)
        links = decoded_str.splitlines()
        for link in links:
            link = urlparse(link.decode("utf-8"))
            tmp = self.parse_one_link_obj(link)
            if tmp:
                yield tmp

    def parse_vmess(self, text):
        decoded_str = self.b64decode(text)
        links = decoded_str.splitlines()
        for link in links:
            link = urlparse(link.decode("utf-8"))
            tmp = self.parse_one_link_obj(link)
            if tmp:
                yield tmp

    def parse_list(self, text):
        for line in text.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("/"):
                continue
            try:
                rule, addr, do = line.split(",")
            except ValueError:
                continue
            match rule:
                case "host":
                    rule = "DOMAIN"
                case "ip-cidr":
                    rule = "IP-CIDR"
                case "host-suffix":
                    rule = "DOMAIN-SUFFIX"
                case "host-keyword":
                    rule = "DOMAIN-KEYWORD"
                case _:
                    continue
            match do:
                case "DIRECT":
                    do = "直连"
                case "Proxy":
                    do = "PROXY"
                case "REJECT":
                    do = "禁连"
                case "OutSide":
                    do = "Apple OutSide"
                case _:
                    pass
            # LOGGER.debug("%s,%s,%s", rule, addr, do)
            yield (rule, addr, do)
