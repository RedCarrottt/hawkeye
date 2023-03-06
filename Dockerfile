FROM redcarrottt/hawkeye:latest
EXPOSE 3000-3001

WORKDIR /home/hawkeye/hawkeye
CMD ["python3", "./hawkeye.py"]
