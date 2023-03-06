FROM redcarrottt/hawkeye:latest
EXPOSE 3000-3001

WORKDIR /home/hawkeye/hawkeye
RUN git pull origin master
CMD ["git", "pull", "origin", "master"]
CMD ["python3", "./hawkeye.py"]
