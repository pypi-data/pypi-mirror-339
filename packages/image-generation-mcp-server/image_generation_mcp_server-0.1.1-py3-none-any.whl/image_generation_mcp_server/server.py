from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import requests
import json
import os

mcp = FastMCP("image_generation")


@mcp.tool()
def generate_image_url_from_text(description : str,
                                 model: str = "MusePublic/489_ckpt_FLUX_1"
                                 ) -> list[TextContent]:
    """Generate an image from the input description using ModelScope API, it returns the image URL.

    Args:
        description: the description of the image to be generated, containing the desired elements and visual features.
        model: the model name to be used for image generation, default is "MusePublic/489_ckpt_FLUX_1".
    """


    url = 'https://api-inference.modelscope.cn/v1/images/generations'
    token = os.environ.get("MODELSCOPE_API_KEY")
    payload = {
        'model': model,  # ModelScope Model-Id, 必填项
        'prompt': description  # 必填项
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url,
                                 data=json.dumps(
                                     payload, ensure_ascii=False).encode('utf-8'),
                                 headers=headers)

        response_data = response.json()
        if 'images' in response_data.keys():
            res= response_data['images'][0]['url']
        else:
            res = str(response_data)

    except Exception as e:
        res = "error:" + str(e)
        print(f"Error: {e}")
    return [TextContent(type="text", text=res)]


# 设置服务入口点，使其可以通过uvx运行
if __name__ == "__main__":
    mcp.run(transport='stdio')
