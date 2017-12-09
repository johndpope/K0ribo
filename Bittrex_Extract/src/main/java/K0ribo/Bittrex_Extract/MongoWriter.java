package K0ribo.Bittrex_Extract;

import org.bson.Document;

import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.IndexOptions;

public class MongoWriter {
	private MongoClient mongoClient;
	private MongoDatabase databse;

	public MongoWriter(String url, int port, String db) {
		super();
		this.mongoClient = new MongoClient(url, port);
		this.databse = mongoClient.getDatabase(db);
	}
	
	public void writeDocument(String collection, Document document){
		this.databse.getCollection(collection).insertOne(document);
		this.databse.getCollection(collection).createIndex(new BasicDBObject("timestamp", 1), new IndexOptions().unique(true));
	}

}
