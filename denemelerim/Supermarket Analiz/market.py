#%% kütüphaneleri getir
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% dosyayı yükle
data = pd.read_csv('marketdata.csv')

#%% test
print(data.head())
print(data.info())
# %% Data temizliği 
print(data.isnull().sum()) #kayıp değerleri gör
data = data .drop_duplicates() #tekrar eden verileri sil
print(data.info())

# %% temel istatistik özetleri
print(data.describe())
mean_groos_income = data ['gross income'].mean()
print(f"Ortalama brüt gelir : {mean_groos_income:.2f}")


# %% şube bazında satışların analizi
branch_sales = data.groupby('Branch')['gross income'].sum()

branch_mean = data.groupby('Branch')['gross income'].mean()
print ("Şube bazında brüt gelir: \n", branch_mean)
best_branch = branch_mean.idxmax()
print(f"En iyi performansa sahip şube: {best_branch}")


# %%kategori bazında satış analizi
category_sales = data.groupby('Product line')['gross income'].sum().sort_values(ascending=False)
top_categories = category_sales.head(3)
print("Ürün grubuna göre brüt:\n",category_sales)

top_categories = category_sales.head(3)
print("Top 3 ürün satırı:\n", top_categories)
# %% Müşteri ve şehir analizi
customer_type_sales = data.groupby('Customer type') ['gross income'].sum()
print("Müşteri türüne göre ortalama gelir:\n", customer_type_sales)

city_sales = data.groupby('City')['gross income'].sum()
print("Ortalama şehire göre gelir:\n",city_sales)
# %% Veriyi görselleştirme
branch_sales.plot(kind='bar', title ='Ortalama şube geliri')
plt.ylabel('Brüt gelir')
plt.show()

top_categories.plot(kind='bar', color='orange', title='Top 3 Kategori geliri')
plt.ylabel('Brüt Gelir')
plt.show()
# %% Seaborn kullanarak gelişmiş görselleme
plt.figure(figsize=(8,5))
sns.histplot(data['gross income'], bins=20, kde=True)
plt.title('Brüt gelirin dağılımı')
plt.xlabel('Brüt gelir')
plt.show()
#%%şubelere göre brüt gelir dağılımı 
plt.figure(figsize=(8,5))
sns.boxplot(x='Branch', y='gross income', data=data)
plt.title('Şubelere göre brüt gelir dağılımı')
plt.show()
#%% ürün grubuna göre satış dağılımı
plt.figure(figsize=(8,6))
sns.boxplot(x='Product line', y='Sales', data=data)
plt.title('Ürün grubuna göre satış dağılımı')
plt.xticks(rotation=45)
plt.show()

#%% müşteri puanı dağılımı
plt.figure(figsize=(8,6))
sns.histplot(data['Rating'], bins=10, kde=True)
plt.title('Müşteri Puan dağılımı')
plt.show()
#%% saçılım grafiği: miktar ve brüt gelir ilişkisi
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='Quantity', y='gross income', hue='Product line')
plt.title('Miktar ve brüt gelir ilişkisi')
plt.xlabel('Miktar')
plt.ylabel('Brüt gelir')
plt.show()

#%% Türe göre müşteri puanı (normal ve üye olan)
plt.figure(figsize=(8,6))
sns.boxplot(x='Customer type', y='Rating', data=data)
plt.title('Türe göre müşteri puanlaması')
plt.show()

#%% ödeme türüne göre analiz
plt.figure(figsize=(8,6))
sns.histplot(data['Payment'], bins=10, kde=True)
plt.title('ödeme türüne göre müşteri dağılımı')
plt.show()

#%% ödeme türüne göre satış toplamları
data.groupby("Payment")["Sales"].sum().sort_values(ascending=False)

#%% ödeme türlerinin adetleri 
# e cüzdanlar en sık kullanılan ödeme yöntemi olmasına rağmen nakit ödemeler daha yüksek işlem ücretlerine neden olur buda toplam satış gelirinin nakit ödemelerle daha iyi karşılandığı anlamına gelir 
data["Payment"].value_counts()
#%% Şehirlere göre satış oranları
data.groupby("City")["Sales"].sum().sort_values(ascending=False)

#%% Şehir başına satış ortalamaları
data.groupby("City")["Sales"].mean().sort_values(ascending=False)
#yangondaki gelirin yüksek sepet değerinden ziyade yüksek işlem sıklığından kaynaklandığını 
# Naypyitaw gibi şehirlerin ise işlem başına daha yüksek değer ürettiğini gösteriyor


#%% kategori bazlı çalışma 
data.groupby("Product line")["Sales"].agg(["sum","mean","count"])

#%% kategori ortalamaları ortalaması 320 den fazla olan kategorileri getir
avg_sales = data.groupby("Product line") ["Sales"].mean()
avg_sales[avg_sales > 320 ]

#%% aylık satışları getir 1. ay 
data["Date"] = pd.to_datetime(data["Date"]) # date aylara çevirme 
data["month"] = data["Date"].dt.month # date aylara çevirme 
data[data["month"] == 1] # 1.aya ait veriyi yazdırma 

#%% aylık bazda ödeme tipi cash olanları getir
data[(data["month"] == 1 ) & (data["Payment"]== "Cash")] 
#%% ödeme tipi cash olanların toplam alışveriş sayısını getir
jan_cash = data[(data["month"] == 1) & (data["Payment"] == "Cash")]
jan_cash["Sales"].count()

#%% korelasyon analizi
data_encoded=pd.get_dummies(data)
corr=data_encoded.corr()
print("Korelasyon matris: \n",corr)

# %%Korealsyon sıcaklık haritası 
data_numeric = data.select_dtypes(include='number')
corr1=data_numeric.corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr1, annot =True, cmap='coolwarm')
plt.title('korelasyon sıcaklık haritası')

# %% Zamansal analiz 
print(data['Date'].head(10))
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, errors='coerce')
data['Month'] = data['Date'].dt.month

monthly_sales = data.groupby('Month')['gross income'].sum()
monthly_sales.plot(kind='line', marker = 'o', title='Aylık Brüt Gelir')
plt.ylabel('Brüt gelir')
plt.show()
# %% Pivot analizi
pivot_table = pd.pivot_table(data, values='gross income', index='Branch', columns='Customer type', aggfunc='sum')
print(pivot_table)
pivot_table.plot(kind='bar',figsize=(8,6), title='Şube ve müşteri tipine göre brüt gelir')
plt.ylabel('Brüt gelir')
plt.show()

# %%
