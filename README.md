# Student List API - API Security Training Platform

## Overview
This is an **intentionally vulnerable** web application designed to teach students about API security vulnerabilities and attack techniques. 

⚠️ **DO NOT USE IN PRODUCTION** - This application lacks security controls on purpose!
8. **XSS Vulnerabilities** - Scripts can be injected in text fields
9. **NoSQL Injection** - JSON injection in extra fields
10. **Data Tampering** - Direct modification of any data

---

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
cd WEB\ training
docker-compose up --build
```

Then open: `http://localhost:5000`

### Option 2: Manual Python Setup
```bash
cd WEB\ training
pip install -r requirements.txt
python app.py
```

Then open: `http://localhost:5000`

---

## 🔗 API Endpoints

### GET /api/students
Retrieve all students
```bash
curl http://localhost:5000/api/students
```

### PUT /api/students
Add a new student (NO VALIDATION!)
```bash
curl -X PUT http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","student_id":"STU-001","email":"john@example.com"}'
```

### PATCH/PUT /api/students/<id>
Update a student (NO AUTH!)
```bash
curl -X PATCH http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe"}'
```

### DELETE /api/students/<id>
Delete a student (ANYONE CAN DELETE!)
```bash
curl -X DELETE http://localhost:5000/api/students/1
```

---

## 🎯 Teaching Scenarios

### 1. Mass Assignment Attack
Show students how to inject extra fields:
```json
{
  "name": "Hacker",
  "student_id": "HACK-001",
  "role": "admin",
  "permissions": ["read", "write", "delete"]
}
```

### 2. XSS (Cross-Site Scripting)
Have students inject JavaScript:
```json
{
  "name": "<img src=x onerror='alert(\"XSS\")'>",
  "student_id": "<script>alert('XSS')</script>"
}
```

### 3. NoSQL Injection
Test NoSQL injection in the extra data field:
```json
{
  "name": "Hacker",
  "extra_field": {
    "$where": "1==1"
  }
}
```

### 4. Brute Force IDs
Students can delete/modify students by guessing IDs:
```bash
for i in {1..100}; do
  curl -X DELETE http://localhost:5000/api/students/$i
done
```

### 5. Data Tampering
Modify any student with PATCH request:
```bash
curl -X PATCH http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Hacker","student_id":"ADMIN","grade":"A+"}'
```

### 6. Large Payload Attack
Test DoS with large payloads:
```bash
python -c "
import requests
huge = 'A' * 1000000
requests.put('http://localhost:5000/api/students',
  json={'name': huge, 'student_id': huge}
)
"
```

---

## 🧪 Built-in Test Functions

The frontend includes test buttons:

- **Test: Add 5 Students** - Demonstrates rapid API calls
- **Test: Large Payload** - Tests size limits
- **Test: Special Characters** - Tests XSS and injection
- **Clear All Data** - Resets the database

---

## 📝 Security Vulnerabilities Explained

| Vulnerability | Location | Impact | Fix |
|---|---|---|---|
| No Input Validation | `app.py` routes | Accept malicious data | Validate & sanitize |
| No Authentication | All endpoints | Anyone can access | Add login/API keys |
| No Authorization | All endpoints | Any user can modify | Add role checks |
| Predictable IDs | Sequential IDs | Easy to guess/brute force | Use UUID/random IDs |
| No Rate Limiting | All endpoints | DDoS possible | Add rate limiting |
| Error Exposure | Exception handling | Info leakage | Generic error messages |
| Debug Mode | `app.run(debug=True)` | Stack traces exposed | Disable in production |
| CORS Open | No CORS config | Cross-origin attacks | Restrict origins |

---

## 🛡️ Secure Version Features

Students should then learn to fix these vulnerabilities:

```python
# ✅ Proper Input Validation
if not isinstance(student['name'], str) or len(student['name']) > 100:
    return error()

# ✅ Authentication
@require_auth
def manage_students():
    pass

# ✅ Authorization
if current_user.id != student['created_by']:
    return forbidden()

# ✅ Rate Limiting
@limiter.limit("10 per minute")
def api_endpoint():
    pass

# ✅ Secure IDs
import uuid
"id": uuid.uuid4()

# ✅ Whitelist Fields
allowed_fields = {'name', 'student_id', 'email', 'grade'}
student = {k: v for k, v in data.items() if k in allowed_fields}
```

---

## 🔍 Monitoring Attacks

Check `students.json` to see all data that was added:
```bash
cat students.json
```

The database file stores everything without encryption!

---

## 📖 Lesson Plan

**Week 1:**
- Students explore the UI and add legitimate data
- Explain each vulnerability shown on the page

**Week 2:**
- Students perform basic attacks (XSS, NoSQL injection)
- Capture screenshots of successful attacks
- Document findings

**Week 3:**
- Students write a "secure" version
- Compare with intentional vulnerabilities
- Present security improvements

**Week 4:**
- Students perform penetration testing exercises
- Write security reports
- Discuss best practices

---

## 🐛 Debug Tips

### Check Debug Mode
The app runs with Flask debug mode enabled (intentional vulnerability)
```python
app.run(debug=True)  # Shows stack traces!
```

### Monitor Requests
Use browser DevTools Network tab to see:
- Request/Response headers
- Body content
- Timing information

### Test with curl/Postman
```bash
# Monitor all requests
curl -v http://localhost:5000/api/students

# Use Postman to craft custom requests
```

---

## 📚 Additional Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OWASP Top 10 Web Vulnerabilities](https://owasp.org/www-project-top-ten/)
- [API Security Best Practices](https://swagger.io/blog/api-security/)
- [CWE-200: Information Exposure](https://cwe.mitre.org/data/definitions/200.html)

---

## 📞 Support

For questions or suggestions about this training material, please refer to the security training documentation.

**Happy Learning! 🎓**
