from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
 
import shutil, time, imghdr, os

class Handler(FileSystemEventHandler):
	def __init__(self):
		self.__HOME = str(Path.home())
		if not os.path.isdir(os.path.join(self.__HOME, "File_Handler")):
			self.create_folders()
		self.main_dir = os.path.join(self.__HOME, "File_Handler")
		self.pdf_dst = os.path.join(self.main_dir, "PDFs")
		self.img_dst = os.path.join(self.main_dir, "Pictures")
		self.other_dst = os.path.join(self.main_dir, "Other")
		self.zip_dst = os.path.join(self.main_dir, "ZIPs")
		self.tracked = os.path.join(self.__HOME, "Downloads")

		os.chdir(self.tracked)

	def on_modified(self, event):
		#TODO: Make the function work on downloading files
		if os.path.isfile(event.src_path) and not event.src_path.endswith(".tmp"):
			_, extension = os.path.splitext(event.src_path)
			if extension == ".pdf":
				self.move_file(src=event.src_path, dst=self.pdf_dst)
			elif imghdr.what(event.src_path) and os.path.basename(event.src_path) in os.listdir(os.getcwd()):
				self.move_file(src=event.src_path, dst=self.img_dst)
			elif extension == ".zip":
				self.move_file(src=event.src_path, dst=self.zip_dst)
			elif extension != ".tmp": 
				self.move_file(src=event.src_path, dst=self.other_dst)

	@staticmethod
	def create_folders():
		home = str(Path.home())
		main_path = os.path.join(home, "File_Handler")
		os.mkdir(main_path)
		os.mkdir(os.path.join(main_path, "PDFs"))
		os.mkdir(os.path.join(main_path, "Pictures"))
		os.mkdir(os.path.join(main_path, "Other"))
		os.mkdir(os.path.join(main_path, "ZIPs"))

	@staticmethod
	def move_file(src, dst):
		file = os.path.basename(src)
		dst = os.path.join(dst, file)
		shutil.move(src=src, dst=dst)


event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, event_handler.tracked, recursive=True)
observer.start()

try:
	while True:
		time.sleep(10)
except KeyboardInterrupt:
	observer.stop()
	observer.join()
