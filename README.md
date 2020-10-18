# Backend

Bu repository **Arduino** ile geliştirilen **akıllı mama kabından** alınan veriyi **makine öğrenmesi modelleri** ile işleyip çıktıları mobil uygulamanın kullanmasını sağlayan API yı barındırmaktadır. Kullanılan makine öğrenmesi modelleri *models* klasörünün altında bulunmaktadır. Modellerin nasıl oluşturulduğu ile ilgili detaylı bilgiyi [AI](https://github.com/Dirty-Paws/AI) repository'sinde bulabilirsiniz.

## 1. Kullanılan Teknolojiler

Django Rest Framework ile geliştirildi. Şuan Google App Engine ile deploy edilmiş olup https://dirty-paws.ey.r.appspot.com/ adresinde ulaşılabilir durumdadır.

## 2. Endpointler

- https://dirty-paws.ey.r.appspot.com/remaining/ 
Akıllı mama kabından POST request olarak gönderilen ağırlık bilgisine göre kaptaki mamanın bitmesine kalan tahmini zamanı hesaplamamıza yarar

Örnek POST REQUEST
```
    {
        "id": 1,
        "Food_Amount_gr": 702.0,
        "Location_Id": 1,
        "Longitude": 35.11337,
        "Latitude": 33.933439,
        "Prediction": null
    }
```

Örnek GET REQUEST
```
    {
        "id": 1,
        "Food_Amount_gr": 702.0,
        "Location_Id": 1,
        "Longitude": 35.11337,
        "Latitude": 33.933439,
        "Prediction": 11.995214285714287
    }
```


- https://dirty-paws.ey.r.appspot.com/emergency Kullanıcıların yaptığı acil durum bildirimlerinin yönetimi burada sağlanır

Örnek POST/GET REQUEST
```
    {
        "id": 2,
        "message": "\"Kediye araba çarptı yetişin\"",
        "owner_id": 2,
        "user_id": null,
        "status": 1,
        "image": null,
        "Location_Id": 3,
        "Longitude": 35.113142,
        "Latitude": 33.934319
    }
```


- https://dirty-paws.ey.r.appspot.com/status Akıllı mama kabında mama kalıp kalmadığının durum bilgisi POST Request olarak buraya gönderilir. Uygulama buradaki veriden faydalanarak mama haritasındaki noktaların durumunu günceller

Örnek POST/GET REQUEST
```
{
	"IsFoodFinished":1,
	"Location_Id": 0,
	"Longitude": 35.111503,
	"Latitude": 33.939892,
}
```

## 3. Localde Kurulum

*Windows 10 kullanıcıları için hazırlanmıştır*

Projede MySQL veritabanı kullanılmıştır. Windows üzerinde MySQL Workbench ile kendi veritabanınızı oluşturabilirsiniz. İndirmek için [tıklayın](https://dev.mysql.com/downloads/workbench/) Yeni bir veritabanı oluşturmak için [bu linkteki](https://www.quackit.com/mysql/workbench/create_a_database.cfm) adımları takip edebilirsiniz. 

Eğer PyCharm kullamıyorsanız DB Browser eklentisi veritabanı işlemleriniz konusunda size oldukça yardımcı olacaktır.

Ön gereklilikler Python 3.7.x
Sanal ortam yaratacağımız için virtuelenv bilgisayarımızda kurulu olmalı. Aşağıdaki komut ile kurabilirsiniz.
```pip install virtualenv```
Repository'i klonladığınız klasöre giderek sanal ortam kurulumu için sırasıyla aşağıdaki komutları çalıştırın
```virtualenv env
env\scripts\activate
pip install -r requirements.txt
```
backend/settings.py dosyanındaki ilgili kısımları kendi veritabanı bilgilerinizi kapsayacak şekilde değiştirin.
```
else:
    # Running locally so connect to either a local MySQL instance or connect
    # to Cloud SQL via the proxy.  To start the proxy via command line:
    #    $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '[YOUR-DATABASE]',
            'HOST': '127.0.0.1',
            'USER': '[YOUR-USERNAME]',
            'PORT':3306,
            'PASSWORD': '[YOUR-PASSWORD]',
        }
    }
```

Gerekli bilgileri girdikten sonra aşağıdaki komutlar ile migration işlemimizi tamamlamamız gerekiyor.
```
python manage.py makemigrations
python manage.py migrate
```

Artık Django uygulamamızı yerel sunucu çalıştırabiliriz.
```
python manage.py runserver
```

http://127.0.0.1:8000 adresinden uygulamaya göz atabilirsiniz.

## 4. Google App Engine ile Deploy

Sıradaki aşama olarak uygulamamızı Google Cloud da nasıl deploy edeceğimize bakacağız. İsterseniz Google'ın [kendi dökümantasyonundan](https://cloud.google.com/python/django/appengine) da faydalanabilirsiniz.

Gerekliliklerimiz Şu şekilde
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Cloud SQL Proxy](https://dl.google.com/cloudsql/cloud_sql_proxy_x64.exe)
- Cloud SQL Admin API aktif olmalı
- Faturalandırma hesabı aktif olmalı


Gerekli kurulumları ve ayarları yaptıktan sonra. Terminal üzerinde aşağıdaki komutu çalıştırarak Google Cloud hesabımıza giriş yapıyoruz
```
gcloud auth application-default login
```
Cloud SQL kullanabilmek için Cloud SQL Admin API yı aktif etmemiz lazım
```
gcloud services enable sqladmin
```
Google Cloud Platform üzerinden MySQL Veritabanı örneği oluşturmamız gerekiyor bunun için aşağıdaki linkten faydalanabilirsiniz<br><br>
[Örnek Oluşturma](https://cloud.google.com/sql/docs/mysql/create-instance)<br>
Veritabanı örneğimizi oluşturduktan sonra yine terminale dönerek oluşturduğumuz örnek adı ile birlikte aşağıdaki komutu çalıştırıyoruz.<br>
```
gcloud sql instances describe [ÖRNEK ADI]
```
Az önce çalıştırdığımız komut bize bağlantı ismimizi gösterecek **connectionName** kısmından bağlantı ismimizi kopyalıyoruz ve terminalden cloud_sql_proxy.exe dosyasını indirdiğimiz klasöre gidiyoruz. Aşağıdaki komutu çalıştırarak örneğimize bağlanıyoruz.
```
cloud_sql_proxy.exe -instances="[BAĞLANTI İSMİNİZİ BURAYA GİRİN]"=tcp:3306
```
Google Cloud Platform a dönerek oluşturduğumuz örnek üzerinde bir veritabanı ve bir kullanıcı oluşturacağız. Bunun için aşağıdaki linklerden faydalanabilirsiniz<br><br>
[Yeni veritabanı oluşturma](https://cloud.google.com/sql/docs/mysql/create-manage-databases#create)<br>
[Yeni kullanıcı oluşturma](https://cloud.google.com/sql/docs/mysql/create-manage-users#creating)<br>

tekrardan backend/settings.py dosyasını açıyoruz ve aşağıdaki kısmı google cloud daki bilgilerimize göre değiştiriyoruz.
```
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/[YOUR-INSTANCE-NAME]',
            'USER': '[YOUR-USERNAME]',
            'PASSWORD': '[YOUR-PASSWORD]',
            'NAME': '[YOUR-DATABASE]',
        }
    }
```
Tekrardan migration işlemimizi gerçekleştiriyoruz
```
python manage.py makemigrations
python manage.py migrate
```
Aşağıdaki komut ile bir yönetici hesabı oluşturuyoruz. Sizden kullanıcı adı, email ve parola isteyecek
```
python manage.py createsuperuser
```

Eğer static dosyalarda bir değişiklik yaptıysanız aşağıdaki komutu çalıştırmanız gerekiyor
```python manage.py collectstatic```

Artık uygulamamızı deploy edebiliriz.

```gcloud app deploy```
