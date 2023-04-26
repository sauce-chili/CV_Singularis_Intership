# CV_Singularis_Intership
Test task in Singularis Lab

*Проект содержит код выполненого задания для стажировки в Singularis Lab(CV/ML). Задача состоит в обнаружении заданных объектов на видео с использованием YOLOv5, их выделения и сохранения кадров с выделенными объектами.*

**Требования**
* Python (у меня 3.10.6)
* venv

**Установка**

<pre>
git clone https://github.com/sauce-chili/CV_Singularis_Intership.git
cd CV_Singularis_Intership
</pre>

**Сборка проекта**

Linux
<pre>
chmod +x setup.sh # предоставляет разрешение на выполнение
./setup.sh
source venv/bin/activate
</pre>

Windows(рекомендуется запускать терминал от имени администтратора)
<pre>
.\setup.bat
.\venv\Scripts\activate
</pre>

**Запуск**
<pre>
# на Linux запускать от python3
python .\main.py --in_video "some_video.mp4" --highlighted_object "orange" --out_path "output/" --out_file_name "new_some_video.mp4"
# или
python .\main.py --in_video "some_video.mp4" --highlighted_object "orange" --out_path "output/new_some_video.mp4"
</pre>

Выполнение скрипта может занять довольно большой промежуток времени
