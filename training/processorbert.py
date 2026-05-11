from sentence_transformers import SentenceTransformer
import joblib

#load the sentence transformer model
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
#classify log message using the trained classifier model
classifier_model = joblib.load('models/log_classifier.pkl')



def classify_with_bert(log_message):
   message_embedding = transformer_model.encode(log_message)
   probabilities = classifier_model.predict_proba([message_embedding])[0]
   if max(probabilities) < 0.5:
       return "Unrecognized"
   predicted_class = classifier_model.predict([message_embedding])[0]
   return predicted_class

if __name__ == "__main__":
    logs = [
        "alpha.osapi.com - - [01/Jun/2024:10:00:00 +0000] \"GET /api/v1/resource HTTP/1.1\" 200 1234",
        "GET /api/v1/resource HTTP/1.1\" 200 1234",
        "User User123 logged in",
        "Multiple failed login attempts detected for user User123", 
        "Backup started at 2024-06-01 10:00:00",
        "System updated to version 2.1.0",
    ]
    for log in logs:
        print(f"Log: {log}\nPredicted Class: {classify_with_bert(log)}\n")