import modal

image = modal.Image.debian_slim().pip_install(["requests", "Pillow"])
stub = modal.Stub("face_stretcher", image=image)


@stub.function(
    schedule=modal.Cron("*/2 * * * *"),
    timeout=60 * 60,
    mounts=[modal.Mount.from_local_dir("images/", remote_path="images/")],
    secrets=[modal.Secret.from_name("face-stretcher-secrets")],
)
def main():
    import time
    import os
    import requests

    from PIL import Image
    from io import BytesIO

    def get_current_profile_picture_url(access_token):
        url = "https://slack.com/api/users.profile.get"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("ok"):
                return resp_json["profile"]["image_original"]
            else:
                print(f'Error fetching profile info: {resp_json.get("error")}')
        else:
            print(f"HTTP error: {response.status_code}")
            print(response.text)
        return None

    def download_image(image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Error downloading image: {response.status_code}")
            print(response.text)
            return None

    def modify_image(image):
        width, height = image.size
        new_width = int(width * 1.4)
        stretched_image = image.resize((new_width, height), Image.LANCZOS)

        # Determine dimensions of the crop box
        new_width, new_height = stretched_image.size
        size = min(new_width, new_height)
        left = (new_width - size) / 2
        top = (new_height - size) / 2
        right = (new_width + size) / 2
        bottom = (new_height + size) / 2

        # Crop the image to a square
        cropped_image = stretched_image.crop((left, top, right, bottom))

        return cropped_image

    def upload_image(access_token, image):
        url = "https://slack.com/api/users.setPhoto"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)
        files = {
            "image": img_byte_arr,
        }
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("ok"):
                print("Profile picture updated successfully.")
            else:
                print(f'Error updating profile picture: {resp_json.get("error")}')
        else:
            print(f"HTTP error: {response.status_code}")
            print(response.text)

    def reset_to_base(access_token):
        url = "https://slack.com/api/users.setPhoto"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        files = {
            "image": open("/images/base.jpg", "rb"),
        }
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("ok"):
                print("Profile picture reset successfully.")
            else:
                print(f'Error resetting profile picture: {resp_json.get("error")}')
        else:
            print(f"HTTP error: {response.status_code}")
            print(response.text)

    access_token = os.environ["SLACK_TOKEN"]
    start = time.time()
    print("Starting face stretcher...")
    while True:
        reset_to_base(access_token)
        print("Reset to base image.")
        for _ in range(10):
            image_url = get_current_profile_picture_url(access_token)
            if image_url:
                image = download_image(image_url)
                if image:
                    stretched_image = modify_image(image)
                    upload_image(access_token, stretched_image)

        if time.time() - start > 100:
            # return to prevent timeout
            return


if __name__ == "__main__":
    main()
