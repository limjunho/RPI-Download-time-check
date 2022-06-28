### 모듈 ###
import os # 운영체제에서 제공되는 여러 기능을 파이썬에서 수행 가능
import time # 시간 모듈
import datetime # 날짜 시간 모듈
import subprocess # 파이썬 프로그램 내에서 새로운 프로세스를 스폰하고 여기에 입출력 파이프를 연결하며 리턴코드를 획득 가능
                  # 다른 언어로 만들어진 프로그램을 통합, 제어 가능
import urllib.request as urllib2 # 주어진 url에서 데이터를 가져오는 기본 기능을 제공
import urllib.parse as urlparse # url의 분해, 조립, 변경 등을 처리하는 함수를 제공

######################################################################################################

# url 경로를 통해 동영상(파일)  다운로드
def download_file(url, dest=None):
    # urlopen -> 해당 URL을 열고 데이터를 얻을 수 있는 함수와 클래스를 제공(HTTP 를 통해 웹 서버에 데이터를 얻는 데 많이 사용)
    u = urllib2.urlopen(url, timeout=10) # timeout -> 내부에서 사용하는 모든 블로킹 연산에 사용할 타임아웃 

    # scheme ->URL scheme specifier, netloc -> Network location part, path -> Hierarchical path, query -> Query component, fragment -> Fragment identifie
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url) # 매개변수를 url에서 분리하지 않음

    filename = os.path.basename(path) # 입력받은 경로의 기본 이름을 반환
    if not filename: # filename이 없으면
        filename = 'downloaded.file'
    if dest: # 별도의 변수를 지정(지정하지 않을 시 None)
        filename = os.path.join(dest, filename) # 해당 os 형식에 맞도록 입력 받은 경로를 연결

    # 파일을 다룰 때 with 블록을 통해 명시적으로 close() 메소드를 호출하지 않고도 파일을 닫을 수 있음(코드를 줄일 수 있음)
    with open(filename, 'wb') as f:
        meta = u.info() # url(server)의 정보
        if hasattr(meta, 'getheaders'): # hasattr -> meta에서 'getheaders'가 있는지 확인
            meta_func = meta.getheaders #(있으면)
        else:
            meta_func = meta.get_all # (없으면)
        meta_length = meta_func("Content-Length") # meta_func에서 Content-Length 부분을 튜플로 저장
        file_size = None
        if meta_length: # meta_length가 0이 아니면(값을 가지면)
            file_size = int(meta_length[0]) # 데이터 타입을 int로 변경(Bite)
            print("Download File : {0}".format(url)) # 다운로드 파일
            print("SIZE: {0:5.2f} MB".format(file_size/1024/1024)) # Bite인 file_size 단위를 MB로 변경
            
            file_size_dl = 0
            
            Bite = 1 # 1B = 8bit
            KB = Bite * 1024 # 1KB = 1024B
            x = 4 * KB # x = 4KB
            
            start = datetime.datetime.utcnow().timestamp() # 다운로드 시작 시간(총 다운로드 측정을 위한 시간) 
            bufftime = 0.0    # 버퍼에 다운로드 되는 시간 
            hddtime = 0.0     # 하드에 다운로드 되는 시간 
            print("Downloading...")
            while True: # 무한 반복
                btime = datetime.datetime.utcnow().timestamp() # buff의 다운로드 시간을 측정하기 위한 시간 
                buffer = u.read(x) # 4KB씩 데이터를 읽음
                btime = datetime.datetime.utcnow().timestamp() - btime # 4KB를 buff에 채우는 시간
                bufftime += btime
                file_size_dl += len(buffer) # 반복될 때 마다 버퍼의 길이만큼 늘어남

                htime = datetime.datetime.utcnow().timestamp() #hddtime
                f.write(buffer) # 버퍼의 크기만큼 데이터를 씀
                htime = datetime.datetime.utcnow().timestamp() - htime # 4KB를 hdd에 채우는 시간
                hddtime += htime

                status = "{0}".format(file_size_dl)
                status = int(status) # 데이터 타입 변경
                status_KB = status // 1024 # Bite인 status 단위를 KB로 변경
                status_MB = status_KB // 1024 # KB인 status_KB 단위를 MB로 변경 
                
                b = "\t[{0:5.2f}%]".format(file_size_dl * 100 / file_size) # b -> 다운로드 파일의 전체 크기에서 현재 다운로드 받은 크기의 비율
                #print("Size downloaded in %d second : "%(time.time() - start), status_MB," MB", b) # 다운로드 진행상황 체크

                if int(file_size/1024/10) <= status_KB: # 다운로드를 완료 하였을 때 -> filesize와 다운로드한 KB의 크기가 같은 조건
                    if file_size: # file_size가 0이 아니면(다운로드가 되었을 때)
                        end = datetime.datetime.utcnow().timestamp() - start
                        b = "\t[{0:5.2f}%]".format(file_size_dl * 100 / file_size) # b -> 다운로드 파일의 전체 크기에서 크현재 다운로드 받은 크기의 비율
                        print("Size downloaded in %d second : "%(end),status_KB," KB", b)

                        Mbps = (status * 8) / end / 1000 / 1000 # 총 Mbps
                        print("\n-------총 다운로드 속도-------\n")
                        print("걸린 시간 : ", round(end, 3), "\b초")
                        print("MB/s = ", round(status_MB / end, 3), "MB/s")
                        print("Mbps = ", round(Mbps, 3) , "Mbps")

                        Mbps = (status * 8) / bufftime / 1000 / 1000 # buff의 Mbps
                        print("\n-------buff에 다운로드 되는 속도-------\n")
                        print("걸린 시간 : ", round(bufftime, 3), "\b초")
                        print("MB/s = ", round(status_MB / bufftime, 3), "MB/s")
                        print("Mbps = ", round(Mbps, 3), "Mbps")
                        
                        Mbps = (status * 8) / hddtime / 1000 / 1000 # hdd의 Mbps
                        print("\n-------hdd에 다운로드 되는 속도-------\n")
                        print("걸린 시간 : ", round(hddtime, 3), "\b초")
                        print("MB/s = ", round(status_MB / hddtime, 3), "MB/s")
                        print("Mbps = ", round(Mbps, 3), "Mbps")
                    break

    return filename

######################################################################################################

# main
url = "http://host/uri/video.mp4" # 다운로드 받을 파일의 경로
filename=download_file(url)
