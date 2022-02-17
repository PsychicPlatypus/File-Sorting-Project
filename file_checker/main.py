from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil, time, imghdr, os, pathlib
#pip install watchdog

class Handler(FileSystemEventHandler):
	def __init__(self):
		#TODO: 
		self.__home_main = str(pathlib.Path.home())
		if not os.path.isdir(os.path.join(self.__home_main, "File_Handler")):
			self.create_folders()
		self.main_dir = os.path.join(self.__home_main, "File_Handler")
		self.pdf_dst = os.path.join(self.main_dir, "PDFs")
		self.img_dst = os.path.join(self.main_dir, "Pictures")
		self.other_dst = os.path.join(self.main_dir, "Other")
		self.zip_dst = os.path.join(self.main_dir, "ZIPs")
		self.music_dst = os.path.join(self.main_dir, "Music")
		self.tracked = os.path.join(self.__home_main, "Downloads")

		self.directions = {".pdf": self.pdf_dst, ".zip": self.zip_dst, ".7z": self.zip_dst, ".mp3": self.music_dst,
                    	".m4a": self.music_dst, ".FLAC": self.music_dst, ".WAV": self.music_dst}
		os.chdir(self.tracked)


	def on_modified(self, event):
		if os.path.isfile(event.src_path) and not event.src_path.endswith(".tmp") and not event.src_path.endswith(".crdownload"):
			_, extension = os.path.splitext(event.src_path)
			if extension in self.directions.keys():
				self.move_file(src=event.src_path, dst=self.directions.get(extension))
			elif imghdr.what(event.src_path) and os.path.basename(event.src_path) in os.listdir(os.getcwd()):
				self.move_file(src=event.src_path, dst=self.img_dst)
			elif extension != ".tmp": 
				self.move_file(src=event.src_path, dst=self.other_dst)

	@staticmethod
	def create_folders():
		home = str(pathlib.Path.home())
		main_path = os.path.join(home, "File_Handler")
		os.mkdir(main_path)
		os.mkdir(os.path.join(main_path, "PDFs"))
		os.mkdir(os.path.join(main_path, "Pictures"))
		os.mkdir(os.path.join(main_path, "Other"))
		os.mkdir(os.path.join(main_path, "ZIPs"))
		os.mkdir(os.path.join(main_path, "Music"))

	@staticmethod
	def move_file(src, dst):
		file = os.path.basename(src)
		dst = os.path.join(dst, file)
		shutil.move(src=src, dst=dst)

def main():
	start_time = time.time()
	event_handler = Handler()
	observer = Observer()
	observer.schedule(event_handler, event_handler.tracked, recursive=True)
	observer.start()

	print("CTRL + C to exit...")
	try:
		while True:
			time.sleep(10)
	except KeyboardInterrupt:
		observer.stop()
		observer.join()
	print(f"Handling over.\nRuntime -> {time.time() - start_time}")


if __name__ == "__main__":
	main()
 