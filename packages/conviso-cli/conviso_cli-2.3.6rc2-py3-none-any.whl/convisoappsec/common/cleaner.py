import os
import shutil
import tempfile
import docker


class Cleaner:
    """Responsible for cleaning temporary files, Docker containers, images, and volumes."""

    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Error initializing Docker client: {e}")
            self.client = None

    def cleanup(self):
        """Performs full cleanup: tmp files, containers, images, volumes."""
        try:
            self.perform_tmp_cleanup()
            self.remove_containers()
            self.remove_images()
            self.remove_volumes()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def perform_tmp_cleanup(self):
        """Cleans the temp directory and 'conviso-output-' dirs in the current directory."""
        tmp_dir = tempfile.gettempdir()

        # Clean system temp directory
        try:
            for filename in os.listdir(tmp_dir):
                file_path = os.path.join(tmp_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception:
                    pass
        except Exception:
            pass

        # Clean conviso-output-* directories
        try:
            for filename in os.listdir("."):
                dir_path = os.path.join(".", filename)
                if os.path.isdir(dir_path) and filename.startswith("conviso-output-"):
                    try:
                        shutil.rmtree(dir_path)
                    except Exception:
                        pass
        except Exception:
            pass

    def remove_containers(self):
        if not self.client:
            return

        for container in self.client.containers.list(all=True):
            try:
                container.remove(force=True)
            except Exception as e:
                print(f"Error removing container {container.name}: {e}")

    def remove_images(self):
        if not self.client:
            return

        for image in self.client.images.list():
            if image.tags and any(tag.startswith("public.ecr.aws/convisoappsec/") for tag in image.tags):
                try:
                    self.client.images.remove(image.id, force=True)
                except Exception as e:
                    print(f"Error removing image {image.tags}: {e}")

    def remove_volumes(self):
        if not self.client:
            return

        for volume in self.client.volumes.list():
            try:
                if volume.name.startswith('conviso-cli'):
                    volume.remove()
            except Exception:
                continue
