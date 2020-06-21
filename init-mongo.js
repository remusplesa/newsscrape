db.createUser({
    user: 'admin',
    pwd: 'admin',
    roles: [{
        role: 'readWrite',
        db: 'newsApp'
    }]
})
db.createCollection('articles')
db.articles.distinct('source')
db.createCollection('keywords')