package K0ribo.Bittrex_Extract;

import java.io.FileReader;
import java.util.Iterator;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import wrapper.Bittrex;

/**
 * Hello world!
 *
 */
public class App 
{
	//args[0] = path to settings.json
    public static void main( String[] args )
    {
        JsonParser parser = new JsonParser();
        try{
        	JsonObject settings = (JsonObject) parser.parse(new FileReader(args[0]));
        	JsonObject mongoSettings = settings.get("mongodb").getAsJsonObject();
        	MongoWriter mongoWriter = new MongoWriter(mongoSettings.get("url").getAsString(), mongoSettings.get("port").getAsInt(), mongoSettings.get("db").getAsString());
        	
        	Iterator<JsonElement> exchanges = settings.get("exchanges").getAsJsonArray().iterator();
        	while(exchanges.hasNext()){
        		JsonObject exchange = exchanges.next().getAsJsonObject();
        		Bittrex bittrex = new Bittrex(exchange.get("api_key").getAsString(), exchange.get("api_secret").getAsString(), 2, 5);
        		Iterator<JsonElement> markets = exchange.get("markets").getAsJsonArray().iterator();
        		while(markets.hasNext()){
        			new Extractor(exchange.get("platform").getAsString(), markets.next().getAsString(), settings.get("interval").getAsInt(), bittrex, mongoWriter);
        		}
        	}
        }catch (Exception e) {
			e.printStackTrace();
		}
    }
}
