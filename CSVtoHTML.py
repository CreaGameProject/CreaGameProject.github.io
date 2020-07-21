import sys
import os
import re
import csv
import urllib.error
import urllib.request

def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

#sampleURL https://drive.google.com/open?id=1hoCCOf_Mmd9yhFFI4ECzImlx52K1dyut
def urlConv(url):
    if 'id=' in url:
        id=url.split('id=')[1]
        return 'https://drive.google.com/uc?id='+id


#引数一覧
replacedNames=['displayName','coments','DepartmentsName','imageName','links']

departmentDict={
    "プログラマー" : "prog",
    "デザイナー" : "des",
    "サウンド" : "sound",
    "プランナー" : "plan",
    "3D" : "3d",
    "未定" : "",
}

wholeString=['',
'''
            </div>
            <!-- End Portfolio Gallery -->
        </div>
        <!-- End Portfolio -->
        <!--========== END PAGE CONTENT ==========-->

        <!--========== FOOTER ==========-->
        <footer class="g-bg-color--dark">
            <!-- Links -->
            <div class="g-hor-divider__dashed--white-opacity-lightest">
                <div class="container g-padding-y-80--xs">
                    <div class="row">
                        <div class="col-sm-2 g-margin-b-20--xs g-margin-b-0--md">
                            <ul class="list-unstyled g-ul-li-tb-5--xs g-margin-b-0--xs">
                                <li><a class="g-font-size-15--xs g-color--white-opacity" href="https://twitter.com/CGP_wakayama">Twitter</a></li>
                                <li><a class="g-font-size-15--xs g-color--white-opacity" href="https://creagamep.wixsite.com/creagamep">ホームページ</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <!-- End Links -->

        </footer>
        <!--========== END FOOTER ==========-->

        <!-- Back To Top -->
        <a href="javascript:void(0);" class="s-back-to-top js__back-to-top"></a>

        <!--========== JAVASCRIPTS (Load javascripts at bottom, this will reduce page load time) ==========-->
        <!-- Vendor -->
        <script type="text/javascript" src="vendor/jquery.min.js"></script>
        <script type="text/javascript" src="vendor/jquery.migrate.min.js"></script>
        <script type="text/javascript" src="vendor/bootstrap/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="vendor/jquery.smooth-scroll.min.js"></script>
        <script type="text/javascript" src="vendor/jquery.back-to-top.min.js"></script>
        <script type="text/javascript" src="vendor/scrollbar/jquery.scrollbar.min.js"></script>
        <script type="text/javascript" src="vendor/swiper/swiper.jquery.min.js"></script>
        <script type="text/javascript" src="vendor/cubeportfolio/js/jquery.cubeportfolio.min.js"></script>
        <script type="text/javascript" src="vendor/jquery.wow.min.js"></script>

        <!-- General Components and Settings -->
        <script type="text/javascript" src="js/global.min.js"></script>
        <script type="text/javascript" src="js/components/header-sticky.min.js"></script>
        <script type="text/javascript" src="js/components/scrollbar.min.js"></script>
        <script type="text/javascript" src="js/components/swiper.min.js"></script>
        <script type="text/javascript" src="js/components/portfolio-3-col.min.js"></script>
        <script type="text/javascript" src="js/components/wow.min.js"></script>
        <!--========== END JAVASCRIPTS ==========-->

    </body>
    <!-- End Body -->
</html>
''']

sampleString1='''<div class=\"s-portfolio__item cbp-item DepartmentsName\">
                    <div class=\"s-portfolio__img-effect\">
                        <img src=\"img/displayName.jpg" alt=\"displayName\">
                    </div>
                    <div class=\"s-portfolio__caption-hover--cc\">
                        <div class=\"g-margin-b-25--xs\">
                            <h3 class=\"g-font-size-18--xs g-color--white g-margin-b-5--xs\">displayName</h3>
                            <p class=\"g-color--white-opacity\">coments</p>
                        </div>
                        <ul class=\"list-inline g-ul-li-lr-5--xs g-margin-b-0--xs\">
                            <li>
                                <a href=\"img/displayName.jpg\" class=\"cbp-lightbox s-icon s-icon--sm s-icon--white-bg g-radius--circle\" data-title=\"displayName\">
                                    <i class=\"ti-fullscreen\"></i>
                                </a>
                            </li>

                            <!--なにかみせたいリンクがあればここに。なければ li ごと消してください。-->
                            <li>
                                <a href=\"links\" class=\"s-icon s-icon--sm s-icon s-icon--white-bg g-radius--circle\">
                                    <i class=\"ti-link\"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                '''

sampleString2='''<div class=\"s-portfolio__item cbp-item DepartmentsName\">
                    <div class=\"s-portfolio__img-effect\">
                        <img src=\"img/displayName.jpg\" alt=\"displayName\">
                    </div>
                    <div class=\"s-portfolio__caption-hover--cc\">
                        <div class=\"g-margin-b-25--xs\">
                            <h3 class=\"g-font-size-18--xs g-color--white g-margin-b-5--xs\">displayName</h3>
                            <p class=\"g-color--white-opacity\">coments</p>
                        </div>
                        <ul class=\"list-inline g-ul-li-lr-5--xs g-margin-b-0--xs\">
                            <li>
                                <a href=\"img/displayName.jpg\" class=\"cbp-lightbox s-icon s-icon--sm s-icon--white-bg g-radius--circle\" data-title=\"displayName\">
                                    <i class=\"ti-fullscreen\"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                '''

matchingString='''
</div>
            <!-- End Portfolio Gallery -->
'''

resultStrings=[]

args = sys.argv

if(args[1]==""):
    print("ファイルをコマンドライン引数にて指定してください。")
    sys.exit()

filePath=args[1]
root, ext = os.path.splitext(filePath)

if(not ext==".csv"):
    print("csvファイルを指定してください。")
    sys.exit()

with open(os.path.dirname(__file__)+'\index.html', encoding='utf-8') as code:
    wholeString=re.split('(</div>\n.*<!-- End Portfolio Gallery -->)',code.read())
    print(wholeString[1])
    for string in wholeString[2:]:
        wholeString[1]+=string

with open(root+ext, encoding="utf_8") as data:
    h=next(csv.reader(data))
    h=next(csv.reader(data))

    for row in csv.reader(data):
        tmpString = sampleString2 if  row[4]=="" else sampleString1
        row[1]=re.sub(r'[\\/:*?"<>|]+','',row[1])
        print(row[1])
        urllib.request.urlretrieve(urlConv(row[4]),os.path.dirname(__file__)+'\img\\'+row[1]+'.jpg')
        for i in range(5):
            if( not(i == 2)):
                print(row[i+1])
                tmpString=re.sub(replacedNames[i],row[i+1],tmpString)
            elif(i==2):
                replacement=""
                for depertment in row[i+1].split(', '):
                    replacement+=' '+departmentDict[depertment]
                
                tmpString=re.sub(replacedNames[i],replacement,tmpString)

        resultStrings.append(tmpString)

resulttxt=wholeString[0]
for result in resultStrings:
    resulttxt+=result
resulttxt+=wholeString[1]

print(resulttxt)

with open(os.path.dirname(__file__)+'/index.html', mode='w',encoding='utf-8') as f:
    f.write(resulttxt)
