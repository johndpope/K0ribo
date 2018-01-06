package K0ribo.Bittrex_Extract;

import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

import wrapper.Bittrex;

/**
 * Hello world!
 *
 */
public class App {
	// args[0] = path to settings.json
	public static void main(String[] args) {
		JsonParser parser = new JsonParser();
		Gson gson = new Gson();
		try {
			JsonObject settings = (JsonObject) parser.parse(new FileReader(args[0]));
			JsonObject sqlSettings = settings.get("sqlite").getAsJsonObject();

			Type listType = new TypeToken<ArrayList<Exchange>>() {
			}.getType();
			List<Exchange> exchanges_db = gson.fromJson(settings.get("exchanges"), listType);
			SQLWriter sqlWriter = new SQLWriter(sqlSettings.get("url").getAsString(), sqlSettings.get("db").getAsString(), exchanges_db);

			Iterator<JsonElement> exchanges = settings.get("exchanges").getAsJsonArray().iterator();
			while (exchanges.hasNext()) {
				JsonObject exchange = exchanges.next().getAsJsonObject();
				Bittrex bittrex = new Bittrex(exchange.get("api_key").getAsString(), exchange.get("api_secret").getAsString(), 2, 5);
				Iterator<JsonElement> markets = exchange.get("markets").getAsJsonArray().iterator();
				while (markets.hasNext()) {
					new Extractor(exchange.get("platform").getAsString(), markets.next().getAsString(), settings.get("interval").getAsInt(), bittrex, sqlWriter);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
