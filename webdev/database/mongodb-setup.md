# MongoDB Setup dan Operasi Dasar

Catatan gabungan dari berbagai topik MongoDB: pengenalan konsep, setup Docker, contoh operasi CRUD, indeks, dan troubleshooting error socket.

---

## Apa itu MongoDB

MongoDB adalah database **NoSQL berbasis dokumen** yang menyimpan data dalam format JSON-like (BSON). Cocok untuk struktur data fleksibel, skala besar, dan integrasi dengan JavaScript/Node.js.

### Konsep Dasar

- **Dokumen**: Satu record data dalam format JSON/BSON.
- **Koleksi (Collection)**: Sekumpulan dokumen, mirip tabel di RDBMS tapi tanpa skema tetap.
- **Database**: Sekumpulan koleksi.

### Kelebihan MongoDB

| Fitur | Penjelasan |
|-------|------------|
| Schema fleksibel | Dokumen dalam satu koleksi bisa punya struktur berbeda |
| Skalabilitas horizontal | Mendukung sharding |
| JSON-like format | Mudah dipakai dengan JavaScript/Node.js |
| Query powerful | Filter, agregasi, pencarian teks, indexing |

---

## Setup MongoDB dengan Docker

### Docker Compose Sederhana

```yaml
services:
  mongodb:
    image: mongo:latest
    container_name: mongo-chk
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: chk

volumes:
  mongo_data:
```

Jalankan:

```bash
docker-compose up -d
```

### Docker Compose dengan Flask App

```yaml
services:
  app:
    build: .
    container_name: flask_app
    ports:
      - "8080:8080"
    depends_on:
      - mongodb
    environment:
      - PORT=8080
      - MONGO_URL=mongodb://mongodb:27017
    volumes:
      - .:/app

  mongodb:
    image: mongo:6.0
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

---

## Operasi Dasar MongoDB

### Insert

```js
db.users.insertOne({ name: "Andi", age: 25, city: "Jakarta" });

db.users.insertMany([
  { name: "Budi", age: 30, city: "Bandung" },
  { name: "Citra", age: 22, city: "Surabaya" }
]);
```

### Query

```js
db.users.find();
db.users.find({ city: "Jakarta" });
db.users.find({ age: { $gt: 25 } });
db.users.findOne({ name: "Alice" });
```

### Update

```js
db.users.updateOne(
  { name: "Andi" },
  { $set: { age: 26 } }
);

db.users.updateOne(
  { name: "Budi" },
  { $inc: { age: 1 } }
);
```

### Delete

```js
db.users.deleteOne({ name: "Citra" });
db.users.deleteMany({ isActive: false });
```

### Embedded Document dan Array

```js
db.orders.insertOne({
  orderId: 1,
  customer: { name: "Andi", email: "andi@gmail.com" },
  items: [
    { product: "Laptop", price: 12000000 },
    { product: "Mouse", price: 200000 }
  ],
  total: 12200000
});

// Query nested field
db.orders.find({ "customer.email": "andi@gmail.com" });

// Array query
db.users.find({ skills: "MongoDB" });
db.users.find({ skills: { $all: ["JavaScript", "MongoDB"] } });
```

### Aggregation

```js
// Group by city
db.users.aggregate([
  { $group: { _id: "$city", totalUser: { $sum: 1 } } }
]);

// Average age
db.users.aggregate([
  { $group: { _id: null, avgAge: { $avg: "$age" } } }
]);

// Match + group
db.users.aggregate([
  { $match: { city: "Jakarta" } },
  { $group: { _id: null, count: { $sum: 1 } } }
]);
```

---

## Index di MongoDB

Index mempercepat pencarian, tapi menambah beban storage dan write.

### Jenis Index

| Jenis | Kegunaan |
|-------|----------|
| Single Field | Index pada satu field |
| Compound | Beberapa field sekaligus |
| Text | Pencarian full-text |
| Hashed | Untuk sharding |
| TTL | Data kadaluarsa otomatis |
| Wildcard | Field dinamis |

### Membuat dan Menghapus Index

```js
// Single field unique
db.users.createIndex({ email: 1 }, { unique: true });

// Compound
db.damages.createIndex({ pc: 1, categoryName: 1 });

// Drop satu index
db.users.dropIndex("email_1");

// Drop semua index kecuali _id
db.users.dropIndexes();
```

### Cek Index

```js
db.users.getIndexes();
db.users.aggregate([{ $indexStats: {} }]);
```

---

## Troubleshooting: MongoDB Crash Socket Error

Error umum saat MongoDB di Docker:

```
Failed to unlink socket file /tmp/mongodb-27017.sock: Operation not permitted
```

### Penyebab

- Sisa file socket dari proses sebelumnya.
- Permission `/tmp` tidak `1777`.
- Container berjalan sebagai non-root.

### Solusi Cepat

```bash
# Cek proses lain
ps aux | grep mongod
ss -lpn | grep 27017

# Perbaiki permission /tmp dan hapus socket lama
sudo chmod 1777 /tmp
sudo rm -f /tmp/mongodb-27017.sock

# Restart container
docker restart <nama_container_mongo>
```

### Solusi Permanen: Nonaktifkan Unix Socket

Buat `mongod.conf`:

```yaml
net:
  bindIp: "*"
  unixDomainSocket:
    enabled: false
```

Mount di `docker-compose.yml`:

```yaml
services:
  mongo:
    image: mongo:8.0
    command: ["--config", "/etc/mongod.conf"]
    volumes:
      - ./mongod.conf:/etc/mongod.conf:ro
      - ./data:/data/db
```

---

## Contoh Desain Database: Lab Animasi

Database `lab_animasi` dengan koleksi:

- `categories`: kategori peralatan.
- `damages`: catatan peralatan rusak per PC.
- `usage_reports`: laporan penggunaan ruangan.
- `room_bookings`: booking ruangan.
- `booking_slots`: slot per jam untuk cek bentrok.
- `schedule_slots`: jadwal kuliah.

Contoh pembuatan koleksi dengan validator:

```js
use lab_animasi

db.createCollection("categories", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name"],
      properties: {
        name: { bsonType: "string", minLength: 1 }
      }
    }
  }
});

db.categories.createIndex({ name: 1 }, { unique: true });
```

---

## Related

- [[redis-upstash]]
- [[supabase]]
- [[index]]
