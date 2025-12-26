# PlayerProfileScreen UI vs Database Schema Mapping

## Database Schema (PostgreSQL/Supabase)

### `users` table:
```sql
- id (VARCHAR(36), PRIMARY KEY)
- email (VARCHAR(255), UNIQUE)
- password_hash (VARCHAR(255))
- first_name (VARCHAR(50))
- last_name (VARCHAR(50))
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### `profiles` table:
```sql
- id (VARCHAR(36), PRIMARY KEY, FK to users.id)
- phone_number (VARCHAR(20), UNIQUE)
- full_name (VARCHAR(100))
- age (INT)
- city (VARCHAR(100))
- gender (VARCHAR(20))
- handedness (VARCHAR(20))
- skill_level (VARCHAR(50))
- sports (JSON)
- playing_style (VARCHAR(100))
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

## PlayerProfileScreen UI Fields

### Fields Collected:
1. **Full Name** (TextInput)
   - State: `fullName`
   - Sent as: `full_name`
   - DB Column: `profiles.full_name` ✅

2. **Age** (TextInput, number-pad)
   - State: `age`
   - Sent as: `age`
   - DB Column: `profiles.age` ✅

3. **City** (Dropdown from admin_cities)
   - State: `city`
   - Sent as: `city`
   - DB Column: `profiles.city` ✅
   - Also sends: `city_id` (reference to admin_cities)

4. **Gender** (Chips: Male, Female, Non-binary, Prefer not to say)
   - State: `gender`
   - Sent as: `gender`
   - DB Column: `profiles.gender` ✅

5. **Handedness** (Chips: Right-handed, Left-handed, Ambidextrous)
   - State: `handedness`
   - Sent as: `handedness`
   - DB Column: `profiles.handedness` ✅

6. **Skill Level** (Chips: Beginner, Intermediate, Advanced, Pro)
   - State: `skillLevel`
   - Sent as: `skill_level`
   - DB Column: `profiles.skill_level` ✅

7. **Favorite Sports** (Multi-select dropdown from admin_game_types)
   - State: `selectedSports` (array)
   - Sent as: `sports` (array)
   - DB Column: `profiles.sports` (JSON) ✅

8. **Playing Style** (Chips: Dinker, Banger, All-court, Net Player, Baseline)
   - State: `playingStyle`
   - Sent as: `playing_style`
   - DB Column: `profiles.playing_style` ✅

9. **Phone Number** (From auth store)
   - State: `user.phoneNumber`
   - Sent as: `phone_number` (in verify-otp call)
   - DB Column: `profiles.phone_number` ✅

---

## Data Flow for New User Registration

### Frontend (PlayerProfileScreen):
```javascript
const profileData = {
    full_name: fullName.trim(),
    age: parseInt(age, 10),
    city: city,
    city_id: cityId,
    gender: gender || undefined,
    handedness: handedness,
    skill_level: skillLevel || undefined,
    sports: selectedSports,  // Array of strings
    playing_style: playingStyle,
};
```

### API Call (verifyOTPWithProfile):
```javascript
POST /auth/verify-otp
{
    phone_number: "+919701829995",
    otp_code: "12345",
    full_name: "Harsha",
    age: 23,
    city: "Hyderabad",
    city_id: "be4a831a-904e-4228-9214-3148da5b96e3",
    gender: "Male",
    handedness: "Right-handed",
    skill_level: "Beginner",
    sports: ["FootBall"],
    playing_style: "All-court"
}
```

### Backend Processing (auth.py):
1. Verify OTP
2. Create user in `users` table
3. Create profile in `profiles` table with all fields
4. Return access_token

---

## Field Mapping Summary

| UI Field | Frontend State | API Field | DB Column | Type | Match |
|----------|---------------|-----------|-----------|------|-------|
| Full Name | `fullName` | `full_name` | `profiles.full_name` | VARCHAR(100) | ✅ |
| Age | `age` | `age` | `profiles.age` | INT | ✅ |
| City | `city` | `city` | `profiles.city` | VARCHAR(100) | ✅ |
| Gender | `gender` | `gender` | `profiles.gender` | VARCHAR(20) | ✅ |
| Handedness | `handedness` | `handedness` | `profiles.handedness` | VARCHAR(20) | ✅ |
| Skill Level | `skillLevel` | `skill_level` | `profiles.skill_level` | VARCHAR(50) | ✅ |
| Sports | `selectedSports` | `sports` | `profiles.sports` | JSON | ✅ |
| Playing Style | `playingStyle` | `playing_style` | `profiles.playing_style` | VARCHAR(100) | ✅ |
| Phone | `user.phoneNumber` | `phone_number` | `profiles.phone_number` | VARCHAR(20) | ✅ |

---

## Additional Fields

### City ID (Reference):
- **Frontend**: `cityId` (from admin_cities dropdown)
- **API**: `city_id`
- **Purpose**: Links to admin_cities table for data integrity
- **Note**: Not stored in profiles table directly, but used for validation

### Avatar (Placeholder):
- **UI**: Camera button on avatar placeholder
- **Status**: Not implemented yet
- **Future**: Will need to add `avatar_url` field to profiles table

---

## Validation Rules

### Required Fields:
- ✅ Full Name (must not be empty)
- ✅ Age (must be a number)
- ✅ City (must be selected from dropdown)

### Optional Fields:
- Gender
- Skill Level
- Sports (can be empty array)

### Default Values:
- Handedness: "Right-handed"
- Playing Style: "All-court"

---

## Conclusion

✅ **ALL FIELDS MATCH PERFECTLY!**

The PlayerProfileScreen UI fields are correctly mapped to the database schema. The field names, types, and data flow are all aligned:

1. Frontend collects data in correct format
2. API sends data with correct field names
3. Backend stores data in correct database columns
4. No mismatches or missing fields

The only thing not implemented yet is the avatar upload functionality, which would require adding an `avatar_url` field to the profiles table in the future.
