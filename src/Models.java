public class Models {
    public static class User {
        public int id;
        public String username;
        public String role;
    }

    public static class Book {
        public int id;
        public String title;
        public String author;
        public boolean isRented;
        public Integer rentedBy;
    }
}
