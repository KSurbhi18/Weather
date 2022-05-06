import weather_api_service
import json 
#with weather_api_service.app.app_context():
    #weather_api_service.db.drop_all()

class UserModel(weather_api_service.db.Model):
    __tablename__ = 'users'
    username = weather_api_service.db.Column(weather_api_service.db.String(255), primary_key=True, nullable=False)
    password = weather_api_service.db.Column(weather_api_service.db.Text, nullable=False)
    full_name = weather_api_service.db.Column(weather_api_service.db.String(255), nullable=False)

    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def to_json(self):
        return dict(
            username=self.username,
            full_name=self.full_name
        )
    
    def get_username(self):
        return self.username


'''class DataModel(weather_api_service.db.Model):
    __tablename__ = 'locations'
    index = weather_api_service.db.Column(weather_api_service.db.Integer,primary_key=True,nullable=False)
    geonameid = weather_api_service.db.Column(weather_api_service.db.Integer)
    country = weather_api_service.db.Column(weather_api_service.db.String(255),nullable=False)
    city = weather_api_service.db.Column(weather_api_service.db.String(255), nullable=False)
    subcountry = weather_api_service.db.Column(weather_api_service.db.String(255))

    def __init__(self,index, geonameid, country, city,subcountry):
        self.index = index
        self.geonameid = geonameid
        self.country = country
        self.city = city
        self.subcountry = subcountry

    def to_json(self):
        return dict(
            index=self.index,
            geonameid=self.geonameid,
            country=self.country,
            city=self.city,
            subcountry=self.subcountry
        )'''

with weather_api_service.app.app_context():
    weather_api_service.db.create_all()
        
        
try:
    import csv

    file = './data/username.csv'
    dict_from_csv = {}

    with open(file, mode='r') as infile:
        reader = csv.reader(infile)
        for i, line in enumerate(reader):
            if i is not 0:
                try:
                    row = list(line)
                    enc_pass = encrypt(secret_key=secret_key, plain_text=row[2])
                    user = UserModel(username=row[1], password=enc_pass, full_name=row[3])
                    weather_api_service.db.session.add(user)
                    weather_api_service.db.session.commit()
                except Exception as e:
                    weather_api_service.db.session.rollback()
except Exception as e:
    pass
print('Users Added')


'''try:
    with open(r"./data/country_data.json",encoding="utf8") as infile:
        location_data = json.loads(infile.read())
        for idx,item in enumerate(location_data):
            try:
                entry = list(item.values())
                data = DataModel(index = idx ,geonameid=entry[1], country=entry[0], city=entry[2],subcountry=entry[3])
                weather_api_service.db.session.add(data)
                weather_api_service.db.session.commit()
            except Exception as e:
                    weather_api_service.db.session.rollback()
except Exception as e:
    pass
print('data added')'''