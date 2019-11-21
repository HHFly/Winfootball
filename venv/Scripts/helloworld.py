import zlib
import urllib2, httplib
def writeFile(fname, data):
    f = open(fname, "w")
    f.write(data)
    f.close()
if __name__ == '__main__':
    httplib.HTTPConnection.debuglevel = 1
    request = urllib2.Request('http://www.163.com/')
    request.add_header('Accept-encoding', 'gzip')# 向服务器请求压缩数据
    opener = urllib2.build_opener()
    f = opener.open(request)
    data = f.read()# 读取页面返回的数据
    f.close()
    print("压缩的数据长度为：%d" %len(data))
    writeFile("a.html", data)
    import StringIO, gzip
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read() # 读取解压缩后数据
    print("解压缩后数据长度为：%d" %len(data2))
    writeFile("aa.html", data2)
