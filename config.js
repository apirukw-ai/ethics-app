// config.js
window.SUPABASE_URL = "https://utwmhcllhgmoqnfbmjwf.supabase.co";
window.SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0d21oY2xsaGdtb3FuZmJtandmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAwMzAyMjEsImV4cCI6MjEwNTYwNjIyMX0.5xguMqgJ7c_uzmJd5-2GikKgvtraJOCG9IZ40y5VNA8";

// สร้าง Supabase Client กลางไว้เรียกใช้
window.supabaseClient = supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);