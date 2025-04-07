
import subprocess

def docker_build(docker_image):
    hash = subprocess.check_output("git rev-parse --short HEAD", shell=True, text=True)
    print(hash.strip())
    hash = hash.strip()
    docker = f'{docker_image}:{hash}'
    return ["docker","build",".","-t",docker]



# def docker_push_ecr():
#     try:
#         ecr_url = f"{aws_account_id}.dkr.ecr.{region}.amazonaws.com"
#         full_image_name = f"{ecr_url}/{repository_name}:{tag}"

#         if login:
#             click.secho(f"🔐 Asumiendo el role: {aws_role_arn}...", fg="cyan")
#             result = subprocess.run(
#                 ["aws", "sts", "assume-role", "--role-arn", aws_role_arn, "--role-session-name", "ECRSession"],
#                 capture_output=True, text=True, check=True
#             )
#             credentials = json.loads(result.stdout)["Credentials"]
#             access_key = credentials["AccessKeyId"]
#             secret_key = credentials["SecretAccessKey"]
#             session_token = credentials["SessionToken"]

#             click.secho("🔑 Obteniendo token de autenticación para ECR...", fg="yellow")
#             subprocess.run(
#                 f"AWS_ACCESS_KEY_ID={access_key} AWS_SECRET_ACCESS_KEY={secret_key} AWS_SESSION_TOKEN={session_token} "
#                 f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {ecr_url}",
#                 shell=True, check=True
#             )

#         click.secho(f"🚀 Construyendo la imagen {full_image_name}...", fg="yellow")
#         subprocess.run(["docker", "build", "-t", full_image_name, dockerfile_path], check=True)

#         click.secho("🏷️ Etiquetando la imagen...", fg="blue")
#         subprocess.run(["docker", "tag", full_image_name, full_image_name], check=True)

#         click.secho(f"📤 Subiendo la imagen a AWS ECR: {full_image_name}...", fg="green")
#         subprocess.run(["docker", "push", full_image_name], check=True)

#         click.secho("✅ Imagen subida con éxito a AWS ECR!", fg="green", bold=True)

#     except subprocess.CalledProcessError as e:
#         click.secho(f"❌ Error: {e}", fg="red", bold=True)
