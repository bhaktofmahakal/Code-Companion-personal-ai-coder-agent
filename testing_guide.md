# AI Code Companion - फीचर्स टेस्टिंग गाइड

इस गाइड का उपयोग AI Code Companion के सभी नए फीचर्स को टेस्ट करने के लिए करें। प्रत्येक फीचर के लिए टेस्ट केस और उदाहरण दिए गए हैं।

## 1. कोड जनरेशन (Code Generation)

**टास्क**: एक सिंपल टू-डू लिस्ट एप्लिकेशन के लिए JavaScript कोड जनरेट करें।

**स्टेप्स**:
1. मोड ड्रॉपडाउन से "Generate Code" चुनें
2. लैंग्वेज ड्रॉपडाउन से "JavaScript" चुनें
3. इनपुट फील्ड में टाइप करें: "Create a simple to-do list application with add, delete, and mark as complete functionality using vanilla JavaScript"
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को HTML, CSS और JavaScript कोड जनरेट करना चाहिए जो एक कार्यात्मक टू-डू लिस्ट एप्लिकेशन बनाता है।

## 2. कोड डिबगिंग (Code Debugging)

**टास्क**: एक बग वाले Python कोड को डिबग करें।

**स्टेप्स**:
1. मोड ड्रॉपडाउन से "Debug Code" चुनें
2. लैंग्वेज ड्रॉपडाउन से "Python" चुनें
3. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test the function
test_list = [10, 20, 30, 40, 50]
print(calculate_average(test_list))  # This works fine

# But this causes an error
empty_list = []
print(calculate_average(empty_list))  # Division by zero error
```
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को ZeroDivisionError की पहचान करनी चाहिए और इसे हैंडल करने के लिए एक सुधारित फंक्शन प्रदान करना चाहिए।

## 3. कोड एक्सप्लेनेशन (Code Explanation)

**टास्क**: एक रिकर्सिव फंक्शन के कार्य को समझाएं।

**स्टेप्स**:
1. मोड ड्रॉपडाउन से "Explain Code" चुनें
2. लैंग्वेज ड्रॉपडाउन से "Python" चुनें
3. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```python
def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]

# Test
print(fibonacci(10))  # 55
```
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को फिबोनाची फंक्शन के कार्य, मेमोइज़ेशन तकनीक और रिकर्सिव कॉल के बारे में विस्तृत व्याख्या प्रदान करनी चाहिए।

## 4. कोड एनालिसिस (Code Analysis)

**टास्क**: एक जटिल फंक्शन का विश्लेषण करें।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Code Analysis" फीचर चुनें
3. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```python
def process_data(data, threshold=0.5, max_iterations=100):
    """
    Process data with complex algorithm.
    """
    results = []
    iterations = 0
    
    for item in data:
        processed = item
        while processed < threshold and iterations < max_iterations:
            processed = processed * 1.1 + 0.05
            iterations += 1
            
        if processed >= threshold:
            results.append((item, processed, iterations))
        else:
            results.append((item, None, iterations))
            
    return {
        'processed_items': len(results),
        'successful': sum(1 for _, p, _ in results if p is not None),
        'iterations': iterations,
        'results': results
    }

# Test with sample data
sample = [0.1, 0.2, 0.3, 0.4, 0.5]
result = process_data(sample)
```
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को कोड की जटिलता, संरचना, और संभावित सुधारों का विश्लेषण प्रदान करना चाहिए।

## 5. टेस्ट जनरेशन (Test Generation)

**टास्क**: एक सिंपल कैलकुलेटर क्लास के लिए यूनिट टेस्ट जनरेट करें।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Generate Tests" फीचर चुनें
3. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```python
class Calculator:
    def add(self, a, b):
        return a + b
        
    def subtract(self, a, b):
        return a - b
        
    def multiply(self, a, b):
        return a * b
        
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को Calculator क्लास के सभी मेथड्स के लिए यूनिट टेस्ट जनरेट करने चाहिए, जिसमें एज केसेस और एक्सेप्शन हैंडलिंग शामिल हो।

## 6. सिक्योरिटी स्कैन (Security Scan)

**टास्क**: एक वेब एप्लिकेशन कोड में सिक्योरिटी वल्नरेबिलिटीज़ की जांच करें।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Security Scan" फीचर चुनें
3. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("<h1>Welcome</h1>")

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable to SQL Injection
    results = db.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")
    
    # Vulnerable to XSS
    return render_template_string(f"<h1>Search results for: {query}</h1>")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Hardcoded credentials
    if username == 'admin' and password == 'password123':
        return "Login successful"
    else:
        return "Login failed"

if __name__ == '__main__':
    app.run(debug=True)
```
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को SQL इंजेक्शन, XSS, हार्डकोडेड क्रेडेंशियल्स और डिबग मोड जैसी सिक्योरिटी वल्नरेबिलिटीज़ की पहचान करनी चाहिए।

## 7. इम्प्लीमेंटेशन प्लानिंग (Implementation Planning)

**टास्क**: एक ऑनलाइन बुकस्टोर एप्लिकेशन के लिए इम्प्लीमेंटेशन प्लान बनाएं।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Plan Implementation" फीचर चुनें
3. इनपुट फील्ड में टाइप करें: "Create an implementation plan for an online bookstore application with user authentication, book catalog, shopping cart, and payment processing"
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को एप्लिकेशन के विभिन्न कंपोनेंट्स के लिए एक स्टेप-बाय-स्टेप इम्प्लीमेंटेशन प्लान प्रदान करना चाहिए।

## 8. प्रोजेक्ट जनरेशन (Project Generation)

**टास्क**: एक सिंपल वेदर एप्लिकेशन प्रोजेक्ट जनरेट करें।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Generate Project" फीचर चुनें
3. इनपुट फील्ड में टाइप करें: "Create a simple weather application that fetches data from a weather API and displays current weather and 5-day forecast for a given city"
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को एक पूर्ण वेदर एप्लिकेशन प्रोजेक्ट जनरेट करना चाहिए, जिसमें HTML, CSS, JavaScript और API इंटीग्रेशन शामिल हो।

## 9. कोड शेयरिंग (Code Sharing)

**टास्क**: एक कोड स्निपेट शेयर करें।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Share Code" फीचर चुनें
3. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```javascript
// Simple utility functions
const utils = {
  sum: (a, b) => a + b,
  multiply: (a, b) => a * b,
  formatCurrency: (amount) => `$${amount.toFixed(2)}`,
  capitalize: (str) => str.charAt(0).toUpperCase() + str.slice(1).toLowerCase(),
  randomInt: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
};

// Test the functions
console.log(utils.sum(5, 10)); // 15
console.log(utils.multiply(5, 10)); // 50
console.log(utils.formatCurrency(123.456)); // $123.46
console.log(utils.capitalize("hELLO")); // Hello
console.log(utils.randomInt(1, 10)); // Random number between 1 and 10
```
4. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को कोड शेयर करने के लिए एक यूनिक URL प्रदान करना चाहिए।

## 10. कस्टम टेम्पलेट (Custom Template)

**टास्क**: एक कस्टम प्रॉम्प्ट टेम्पलेट बनाएं।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Create Template" फीचर चुनें
3. टेम्पलेट नाम फील्ड में टाइप करें: "React Component Generator"
4. टेम्पलेट कंटेंट फील्ड में टाइप करें:
```
Create a React functional component with the following specifications:

Component Name: {{component_name}}
Props: {{props}}
State Variables: {{state}}
Description: {{description}}

Please include:
1. Proper TypeScript types
2. JSDoc comments
3. CSS module styling
4. Unit test file

The component should follow best practices and be optimized for performance.
```
5. "Save Template" बटन पर क्लिक करें

**अपेक्षित परिणाम**: टेम्पलेट सफलतापूर्वक सेव होना चाहिए और ड्रॉपडाउन में दिखाई देना चाहिए।

## 11. सिंटैक्स हाइलाइटिंग (Syntax Highlighting)

**टास्क**: एक कोड स्निपेट को सिंटैक्स हाइलाइटिंग के साथ फॉर्मेट करें।

**स्टेप्स**:
1. "Advanced" बटन पर क्लिक करें
2. "Code Highlighting" फीचर चुनें
3. लैंग्वेज ड्रॉपडाउन से "Java" चुनें
4. इनपुट फील्ड में निम्न कोड पेस्ट करें:
```java
import java.util.ArrayList;
import java.util.List;

public class StreamExample {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");
        names.add("David");
        
        // Using streams to filter and transform data
        List<String> filteredNames = names.stream()
            .filter(name -> name.length() > 4)
            .map(String::toUpperCase)
            .sorted()
            .toList();
            
        System.out.println("Original names: " + names);
        System.out.println("Filtered names: " + filteredNames);
    }
}
```

output:---
```java
import java.util.ArrayList;
import java.util.List;

public class StreamExample {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");
        names.add("David");
        
        // Using streams to filter and transform data
        List<String> filteredNames = names.stream()
            .filter(name -> name.length() > 4)
            .map(String::toUpperCase)
            .sorted()
            .toList();
            
        System.out.println("Original names: " + names);
        System.out.println("Filtered names: " + filteredNames);
    }
}
```

5. सेंड बटन पर क्लिक करें

**अपेक्षित परिणाम**: AI को सिंटैक्स हाइलाइटिंग के साथ फॉर्मेटेड कोड प्रदान करना चाहिए।


- कुछ फीचर्स के लिए Ollama API कनेक्शन की आवश्यकता होती है
- प्रोजेक्ट जनरेशन और कोड शेयरिंग के लिए फाइल सिस्टम एक्सेस की आवश्यकता होती है
- सभी फीचर्स के लिए आवश्यक पायथन मॉड्यूल्स इंस्टॉल होने चाहिए (pygments, fastapi, uvicorn, आदि)

http://127.0.0.1:8000/shared/d81b05c8