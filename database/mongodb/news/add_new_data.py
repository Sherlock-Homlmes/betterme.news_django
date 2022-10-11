from .news_database import *
from .crawl import *
from .seo_process import *
from .imgbb_image_process import *
import io,json


async def test_create_data(url,name,html_type,thumbnail_link,slide_show_link,description,tags):
  ###############done

    #content
    key = test_crawl(url)

    title = key[0]
    content = replace_h1(key[1])
    date = key[2]

    #add internal link
    ul = seo_ul(internal_link(tags,3))
    content = add_str_to_str(content,ul,'<div class="author-info')

    #meta
    meta = crawl_meta(url)
    description = meta[0]
    keywords = meta[1]
    og_image = meta[2]
    print(og_image)

    element = {
    #không cần chỉnh sửa
      'count':0,
      'position': 0,
      'view':0,
      'rate': 0,

      'description':description,
      'keywords':keywords,
      'og_image':og_image,
      'title': title,
      'content': content,
      'date': [date],

    #cần chỉnh sửa
      'name': name,
      'html_type': html_type,
      'description': description,
      'thumbnail_link': thumbnail_link,  
      'slide_show_link': slide_show_link,
      'tags':tags,


    }

    with io.open('main/views/data.json', 'w', encoding='utf-8') as f:
        json.dump(element, f, ensure_ascii=False, indent=4)
    
    return element


async def create_data(url,name,html_type,thumbnail_link,slide_show_link,description,tags):
  ######################done
  check = dtb.find_one({'name':name})
  print(check)
  if check:
    print('already have ',name)
  else:

    #content
    key = crawl(url)

    title = key[0]
    content = replace_h1(key[1])
    date = key[2]

    #add internal link
    ul = seo_ul(internal_link(tags,3))
    content = add_str_to_str(content,ul,'<div class="author-info')

    #meta
    meta = crawl_meta(url)
    if description == "":
      description = meta[0]
    keywords = meta[1]
    og_image = imgbb_image(meta[2])

    if thumbnail_link != "":
      thumbnail_link = imgbb_image(thumbnail_link)
    else:
      crop = crop_image(slide_show_link)
      thumbnail_link = upload_imgbb_image(crop)
      delete_image(crop)
      
    if slide_show_link != "":
      slide_show_link = imgbb_image(slide_show_link)
      tags.insert(0,"hot")

    element = {
    ###element properties
      'count':0,
      'position': 0,
      'view':0,
      'rate': 0,

    ###seo
      'description':description,
      'keywords':keywords,
      'og_image':og_image,
      'title': title,
      'content': content,
      'date': date,

    ###show up
      'name': name,
      'html_type': html_type,
      'description': description,
      'thumbnail_link': thumbnail_link,  
      'slide_show_link': slide_show_link,
      'tags':tags
    }

    #with io.open('data.json', 'w', encoding='utf-8') as f:
        #json.dump(element, f, ensure_ascii=False, indent=4)

    return element
  

#####crawl data

#chỉnh sửa giá trị
url = "https://khoahoc.tv/ban-co-biet-cac-not-san-tren-la-sung-thuc-chat-la-gi-khong-95680"
name = 'ban-co-biet-cac-not-san-tren-la-sung-thuc-chat-la-gi-khong'
html_type = 'normal' #(normal | horror)

thumbnail_link = 'https://e.khoahoc.tv/photos/image/2018/10/18/not-san-tren-la-sung-200.jpg'
slide_show_link = ''
add_ul = False
remove_ahref = False

description = ""

tags = [
###type1: khoa học hàn lâm
#'khoa-hoc',
#'lich-su',
#'dia-ly',
#'sinh-hoc',

###type2: nâng tầm hiểu biết
#'10-van-cau-hoi-vi-sao',
'su-that-thu-vi',
#'1001-bi-an',
#'danh-nhan-the-gioi',
#'kien-truc-doc-dao'
#'the-gioi-dong-vat',

###type3: kiến thức thực tế
'y-hoc-suc-khoe',

]

###test
def fake_data():
  fake_element = test_create_data(url,name,html_type,thumbnail_link,slide_show_link,description,tags)
  print(fake_element)
#fake_data()

###real #####up data lên database
def real_data():
  real_element = create_data(url,name,html_type,thumbnail_link,slide_show_link,description,tags)
  #print(real_element)
  ndb(real_element)
#real_data()

#####lấy data (theo position)
#element = take_ndb(1)

#####update all data (theo position)
#update_ndb(1,element)

#####update data element (theo position) (thứ tự: position, key, value)
#update_element(42,'description','')

#content = '''<h1 class="w3-center w3-padding-64"><span class="w3-tag w3-wide">Khám phá thành cổ bí ẩn trong sa mạc Sahara</span></h1><div class="content-detail textview"><p><strong>Khu vực sa mạc Sahara thuộc Đông Bắc Niger (châu Phi) là vùng đất hầu như nằm ngoài sự hiểu biết của con người.</strong></p><p>Những đụn cát khổng lồ cao chót vót là chướng ngại khó vượt qua. Tuy nhiên, giữa nơi dường như không có sự sống này lại tồn tại tàn tích của một thành phố lớn với nhiều bí ẩn.</p><h2>Thành phố pháo đài giữa cao nguyên</h2><p>Thành phố Djado, đặt theo tên cao nguyên nơi nó được phát hiện, có một số cấu trúc quen thuộc và dễ nhận biết từ các nền văn hóa lân cận, nhưng nhiều công trình vẫn còn bí ẩn với các nhà khảo cổ.</p><p style="text-align:center"><img alt="Thành phố pháo đài Djado." class="lazy" data-src="https://i.ibb.co/nmptNJM/image.jpg" height="454" src="https://i.ibb.co/nmptNJM/image.jpg" width="700" /><br />Thành phố pháo đài Djado.</p><p>Thành phố trên có thể được xây dựng cách nay khoảng từ 800 - 1.000 năm, vào thời điểm nơi đây còn ẩm ướt, nhiều rừng rậm và đất đai màu mỡ. Người ta từng biết một số điều về cư dân sống nơi đây trong quá khứ, nhưng họ có phải là những người xây dựng thành phố này hay không vẫn còn là dấu hỏi.</p><p>Ở Bắc Phi có những khu định cư nằm rải rác, được gọi chung là <em><strong>“ksar”</strong></em>, với những ngôi nhà được xây dựng từ những thân cây cọ, bao quanh bởi một lớp bùn không nung. Theo thời gian, nắng gió sa mạc sẽ làm chúng khô lại và trở nên cứng như sắt.</p><p><strong>Thành phố pháo đài Djado</strong> là một trong những khu định cư như vậy. Nhưng điều khiến Djado khác biệt so với hầu hết các ksar tương tự là kích thước khổng lồ của nó. Vươn lên từ sa mạc, thành phố nổi bật giữa cảnh quan xung quanh, bao quát cả một khu vực rộng lớn, vừa là pháo đài, vừa là trung tâm thương mại nằm dọc theo các tuyến đường hướng tới Libya.</p><p>Những <strong>người Kanuri </strong>ở giữa sa mạc Sahara là cư dân cuối cùng được biết đến của Djado. Tuy nhiên, không có bằng chứng cho thấy, họ đã xây dựng công trình hoành tráng này, nên người ta cho rằng, có thể họ đã kế thừa thành phố từ một nền văn minh chưa được biết đến.</p><p>Do vị trí thuận lợi và khí hậu dễ chịu trong quá khứ, cao nguyên Djado đã chứng kiến sự cư trú của con người trước khi thành phố ra đời rất lâu. Theo các nhà khoa học, con người đã sống trên cao nguyên này cách nay khoảng 60 nghìn năm, còn lưu lại các công trình mỹ thuật bằng đá và các dấu hiệu khác về sự hiện diện của họ.</p><p>Nông nghiệp, chăn nuôi ban đầu cũng để lại dấu vết tại địa điểm này. Dê và cừu được chăn thả ở đây sớm nhất là 7 nghìn năm trước Công nguyên, với những khu định cư đầu tiên được xây dựng.</p><p style="text-align:center"><img alt="Nghệ thuật trên đá mô tả thời phồn thịnh ở cao nguyên Djado." class="lazy" data-src="https://i.ibb.co/BTw47Zz/image.jpg" height="370" src="https://i.ibb.co/BTw47Zz/image.jpg" width="650" /><br />Nghệ thuật trên đá mô tả thời phồn thịnh ở cao nguyên Djado.</p><p>Nhiều bức tranh trên đá được tìm thấy trong dãy núi Aïr ở vùng này có niên đại từ 3.500 TCN đến 2.500 TCN. Chúng miêu tả một cảnh quan rất khác so với ngày nay, đó là một khu vực xanh tươi với thảm thực vật trải dài, cùng nhiều loài động vật sinh sống, trong đó có hươu cao cổ, voi và nhiều thú lớn khác.</p><p>Trong quá trình xây dựng các ksar, người cổ luôn chú trọng đến nhiệt độ thay đổi và điều kiện khắc nghiệt trong vùng, nên việc Djado bị bỏ hoang không có nghĩa là nó bị tàn phá.</p><p>Điểm mấu chốt khiến người dân Kanuri từ bỏ thành phố quê hương dường như là do thiếu nguồn cung cấp nước sạch. Khi cảnh quan xanh tốt biến thành sa mạc, nước ngọt chuyển thành nước lợ, môi trường trở nên quá khắc nghiệt, không ai có thể sống được ở nơi này.</p><h2>Ai xây dựng?</h2><p>Biệt lập với thế giới và được thiết kế để chịu được môi trường sa mạc nên phần lớn công trình thành phố pháo đài Djado vẫn tồn tại đến ngày nay. Những bức tường của chúng đứng sừng sững, đầy kiêu hãnh và nhiều tòa nhà hầu như nguyên vẹn, chỉ thiếu những mái vòm.</p><p>Tuy nhiên, việc tiếp cận thành phố cổ hiện là một thách thức với các nhà khảo cổ. Khu vực này của thế giới rất bất ổn, các bộ lạc đang mâu thuẫn gay gắt vì tranh giành nguồn tài nguyên hạn chế. Có thể các cuộc khai quật trong tương lai sẽ làm sáng tỏ ai là người đã xây dựng thành phố vĩ đại Djado và chúng ta có thể bắt đầu hiểu về con người của nền văn hóa đã mất này của Sahara.</p><p>Người Kanuri, được cho là những cư dân cuối cùng của Djado, đang cư trú tại ngôi làng sa mạc Chirfa gần đó. Hằng năm, họ đều quay lại địa điểm của tổ tiên mình để thu hoạch những quả chà là, bằng cách nào đó vẫn còn mọc xung quanh khu di tích. Có thể người Kanuri là phần còn lại của đế chế Kanem, một nền văn minh vĩ đại đã cai trị vùng trung tâm Sahara từ khoảng năm 700 – 1.300 Công nguyên.</p><p style="text-align:center"><img alt="Người Kanuri, cư dân cuối cùng của Djado." class="lazy" data-src="https://i.ibb.co/gPZ3Nk9/image.jpg" height="496" src="https://i.ibb.co/gPZ3Nk9/image.jpg" width="650" /><br />Người Kanuri, cư dân cuối cùng của Djado.</p><p>Nhưng nguồn gốc của đế chế này rất ít người biết đến, và không có nhiều thông tin về những thế kỷ đầu trị vì của họ. Không rõ liệu Djado có được xây dựng trong thời kỳ này hay nó thực sự còn hiện diện trước cả Kanem.</p><p>Nếu <strong>đế chế Kanem</strong> xây dựng Djado, các cuộc khai quật tại địa điểm này có thể tiết lộ phần lớn nền văn hóa bí ẩn này và cung cấp cái nhìn sâu sắc về những khởi đầu của họ. Nhưng nếu họ chỉ kế thừa Djado, thì chúng ta sẽ có may mắn phát hiện thêm một nền văn hóa mới, được bảo tồn và ẩn giấu nơi sa mạc khô cằn.</p></div><ul style="user-select: auto"><li style="user-select: auto"><a title='Chand Baori - Giếng nước cổ độc đáo với kiến trúc ấn tượng của Ấn Độ' href="https://betterme.news/chand-baori-gieng-nuoc-co-doc-dao-voi-kien-truc-an-tuong-cua-an-do" style="user-select: auto">Chand Baori - Giếng nước cổ độc đáo với kiến trúc ấn tượng của Ấn Độ</a></li><li style="user-select: auto"><a title='"Hạt ma quỷ" từ chiều không gian khác xuất hiện khắp Trái đất?' href="https://betterme.news/hat-ma-quy-tu-chieu-khong-gian-khac-xuat-hien-khap-trai-dat" style="user-select: auto">"Hạt ma quỷ" từ chiều không gian khác xuất hiện khắp Trái đất?</a></li><li style="user-select: auto"><a title='Thực hư về những bí ẩn và hồn ma tồn tại ở Tháp London' href="https://betterme.news/thuc-hu-ve-nhung-bi-an-va-hon-ma-ton-tai-o-thap-london" style="user-select: auto">Thực hư về những bí ẩn và hồn ma tồn tại ở Tháp London</a></li></ul><div class="author-info clearfix"><span class="date">Cập nhật: 21/04/2022</span> <span class="author">Theo GD&amp;TĐ</span></div>'''
#update_element(55,'content',content)

