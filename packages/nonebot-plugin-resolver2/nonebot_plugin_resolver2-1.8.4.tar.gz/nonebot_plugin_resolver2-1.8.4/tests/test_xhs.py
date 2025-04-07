from nonebot import logger


async def test_xiaohongshu():
    """
    xiaohongshu:
    - https://xhslink.com/a/zGL52ubtpJ20
    - https://www.xiaohongshu.com/discovery/item/6469c95c0000000012031f3c?source=webshare&xhsshare=pc_web&xsec_token=ABkMJSd3a0BPMgj5BMkZcggIq1FxU8vYNcNW_-MhfDyq0=&xsec_source=pc_share
    """
    # 需要 ck 才能解析， 暂时不测试
    from nonebot_plugin_resolver2.parsers.xiaohongshu import parse_url

    urls = [
        "https://www.xiaohongshu.com/discovery/item/67cdaecd000000000b0153f8?source=webshare&xhsshare=pc_web&xsec_token=ABTvdTfbnDYQGDDB-aS-b3qgxOzsq22vIUcGzW6N5j8eQ=&xsec_source=pc_share",
    ]
    for url in urls:
        logger.info(f"开始解析小红书: {url}")
        title_desc, img_urls, video_url = await parse_url(url)
        assert title_desc
        logger.debug(f"title_desc: {title_desc}")
        assert img_urls or video_url
        logger.debug(f"img_urls: {img_urls}")
        logger.debug(f"video_url: {video_url}")
        logger.success(f"小红书解析成功 {url}")
