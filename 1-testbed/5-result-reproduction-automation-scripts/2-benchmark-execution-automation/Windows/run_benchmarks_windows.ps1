cd ..\ &&

python .\benchmarks.py --host-platform windows --benchmark jetstream2 &&
python .\benchmarks.py --host-platform windows --benchmark motionmark &&
python .\benchmarks.py --host-platform windows --benchmark speedometer &&

Start-Sleep -Seconds 15 &&

Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"

Start-Sleep -Seconds 60 &&

cd ..\Windows\x-version &&

docker compose -f .\docker-compose-firefox-x-windows-automated-benchmarks.yml up &&

Start-Sleep -Seconds 15 &&

docker compose -f .\docker-compose-firefox-x-windows-automated-benchmarks.yml down &&

Start-Sleep -Seconds 15 &&

cd ..\wayland-version &&

Start-Sleep -Seconds 15 &&

docker compose -f .\docker-compose-firefox-wayland-windows-automated-benchmarks.yml up &&

Start-Sleep -Seconds 15 &&

docker compose -f .\docker-compose-firefox-wayland-windows-automated-benchmarks.yml down
