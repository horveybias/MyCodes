import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.awt.*;
import javax.swing.*;

public class PIT {

    
    private static final String DB_URL = "jdbc:mysql://localhost:3306/student_registration";
    private static final String USER = "root"; // replace with your MySQL username
    private static final String PASS = "horve";

    public static Account[] allAccounts =new Account[10];
    public static int CountAccount = 0;
    public static int countID = 0; 
    public static JTextField nameField, ageField, phonenumberField, yearLevelField, emailField;
    public static JPasswordField passField, passwordFieldLogin;
    public static JTextField emailFielLogin;
    public static String sections[] = {"S1","S2","S3","S4","S5"};
    public static String courses[] = {"(IT) Information Technology","Data Science","Computer Science","Civil Engineering", "Electrical Engineering", "Computer Engineering"};
    public static String gender[] = {"Male","Famale"};
    public static JComboBox<String> secBox, courseBox, genderBox;
    public static JComboBox<String> newgenderBox, newsecBox, newcourseBox;

    public static void main(String[] args){

        JFrame mainframe = new JFrame("student Registration");
        mainframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainframe.setSize(1000, 600);
        mainframe.setResizable(false);
        mainframe.setLayout(null);

        ImageIcon imageicon = new ImageIcon("image.PNG");
        Image Image = imageicon.getImage();
        Image newimage = Image.getScaledInstance(500, 500, java.awt.Image.SCALE_SMOOTH);
        imageicon = new ImageIcon(newimage);
        mainframe.setIconImage(imageicon.getImage());

        JLabel imagLabel = new JLabel();
        imagLabel.setIcon(imageicon);
        imagLabel.setFont(new Font("Arial", Font.BOLD, 16));
        mainframe.add(imagLabel);

        JPanel imagepanel = new JPanel();
        imagepanel.setBackground(Color.lightGray);
        imagepanel.setBounds(0, 0, 500, 600);
        mainframe.add(imagepanel);
        imagepanel.add(imagLabel);

        // label
        JLabel WelcomeLabel = new JLabel(" Student Registration", SwingConstants.CENTER);
        WelcomeLabel.setBounds(600, 50, 300 ,40);
        WelcomeLabel.setFont(new Font("Arial", Font.BOLD, 16));
        mainframe.add(WelcomeLabel);

        // button
        JButton CreateAccountButton = new JButton("CreateAccount");
        CreateAccountButton.setBounds(600, 100, 300, 50);
        CreateAccountButton.addActionListener(e->CreateAccountScreen(mainframe));
        mainframe.add(CreateAccountButton);

        JButton LoginButton = new JButton("Login");
        LoginButton.setBounds(600, 170, 300, 50);
        LoginButton.addActionListener(e->LoginScreen(mainframe));
        mainframe.add(LoginButton);

        JButton ExitButton = new JButton("Exit Program");
        ExitButton.setBounds(600, 240, 300, 50);
        ExitButton.addActionListener(e->System.exit(0));
        mainframe.add(ExitButton);

        mainframe.setVisible(true);

        try (Connection connection = DriverManager.getConnection(DB_URL, USER, PASS)) {
            System.out.println("Connected to the database successfully!");
            // You can now perform database operations here
        } catch (SQLException e) {
            System.out.println("Connection to the database failed!");
            e.printStackTrace();
        }
    }

    // Generate ID number
    public static String generateID() {
        countID++; 
        return "2024-" + String.format("%05d", countID); 
    }

    public static void CreateAccountScreen(JFrame mainframe) {
        mainframe.dispose();
        JFrame CreateAccountFrame = new JFrame("Create Account");
        CreateAccountFrame.setSize(1000, 600);
        CreateAccountFrame.setResizable(false);
        CreateAccountFrame.setLayout(new GridLayout(11,2,0,5));

        // text field
        nameField = new JTextField();
        ageField = new JTextField();
        phonenumberField = new JTextField();
        genderBox = new JComboBox<>(gender);
        secBox = new JComboBox<>(sections);
        courseBox = new JComboBox<>(courses);
        yearLevelField = new JTextField();
        emailField = new JTextField();
        passField = new JPasswordField();
        String newID = generateID();

        
        // label
        CreateAccountFrame.add(new JLabel("Full Name:"));
        CreateAccountFrame.add(nameField);
        CreateAccountFrame.add(new JLabel("Age"));
        CreateAccountFrame.add(ageField);
        CreateAccountFrame.add(new JLabel("Phone Number:"));
        CreateAccountFrame.add(phonenumberField);
        CreateAccountFrame.add(new JLabel("Gender:"));
        CreateAccountFrame.add(genderBox);
        CreateAccountFrame.add(new JLabel("Section:"));
        CreateAccountFrame.add(secBox);
        CreateAccountFrame.add(new JLabel("Course:"));
        CreateAccountFrame.add(courseBox);
        CreateAccountFrame.add(new JLabel("Year Level:"));
        CreateAccountFrame.add(yearLevelField);
        CreateAccountFrame.add(new JLabel("Email: "));
        CreateAccountFrame.add(emailField);
        CreateAccountFrame.add(new JLabel("Create Password: "));
        CreateAccountFrame.add(passField);
        CreateAccountFrame.add(new JLabel("Student ID: "+ newID));
        CreateAccountFrame.add(new JLabel());
       
        // Cancel
        JButton cancel = new JButton("Cancel");
        cancel.addActionListener(e->{
            main(null);
            CreateAccountFrame.dispose();
        });
        CreateAccountFrame.add(cancel);

        // button
        JButton Submit = new JButton("Submit");
        Submit.addActionListener(e -> FinishCreateAccount(CreateAccountFrame, newID));
        CreateAccountFrame.add(Submit);

        CreateAccountFrame.setVisible(true);
    }

    public static void FinishCreateAccount(JFrame CreateAccountFrame, String ID){
        String name = nameField.getText();
        String age = ageField.getText();
        String phonenumber = phonenumberField.getText();
        String gender = (String)genderBox.getSelectedItem();
        String section = (String)secBox.getSelectedItem();
        String course = (String)courseBox.getSelectedItem();
        String yearLevel = yearLevelField.getText();
        String email = emailField.getText();
        String password = new String(passField.getPassword());
        

        if(name.isEmpty() || age.isEmpty() || phonenumber.isEmpty() || email.isEmpty() || yearLevel.isEmpty() || password.isEmpty()){
            JOptionPane.showMessageDialog(null, "All fields are required!", "Information Massage", JOptionPane.ERROR_MESSAGE);
            return;
        }

        for (int i = 0; i < CountAccount; i++) {
            if (allAccounts[i].getName().equals(name)) {
                JOptionPane.showMessageDialog(null, "Account name already exists!", "Information Message", JOptionPane.ERROR_MESSAGE);
                return;
            }
            if (allAccounts[i].getPassword().equals(password)) {
                JOptionPane.showMessageDialog(null, "Account name already exists!", "Information Message", JOptionPane.ERROR_MESSAGE);
                return;
            }
        }

        Account newAccount = new Account(name, age, phonenumber, gender, section, course, yearLevel, email, password, ID);
        allAccounts[CountAccount] = newAccount;
        CountAccount++;
        System.out.println(newAccount);
        System.out.println("Count all accounts: "+CountAccount);
        CreateAccountFrame.dispose();
        main(null);

        try (Connection connection = DriverManager.getConnection(DB_URL, USER, PASS)) {
            String sql = "INSERT INTO accounts (name, age, phone_number, gender, section, course, year_level, email, password, student_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, name);
            preparedStatement.setInt(2, Integer.parseInt(age));
            preparedStatement.setString(3, phonenumber);
            preparedStatement.setString(4, gender);
            preparedStatement.setString(5, section);
            preparedStatement.setString(6, course);
            preparedStatement.setString(7, yearLevel);
            preparedStatement.setString(8, email);
            preparedStatement.setString(9, password);
            preparedStatement.setString(10, ID);
            preparedStatement.executeUpdate();
            System.out.println("Account created and saved to the database.");
        } catch (SQLException e) {
            System.out.println("Error while inserting account into the database.");
            e.printStackTrace();
        }

    }

    public static void LoginScreen(JFrame mainframe){

        JFrame logFrame = new JFrame("login");  
        logFrame.setSize(1000, 600);
        logFrame.setResizable(false);
        logFrame.setLayout(null);

        // label
        JLabel WelcomeLabel = new JLabel("Login to Your Account", SwingConstants.CENTER);
        WelcomeLabel.setBounds(350, 20,300 ,40);
        WelcomeLabel.setFont(new Font("Arial", Font.BOLD, 20));
        logFrame.add(WelcomeLabel);

        JLabel emailLabel = new JLabel("Email");
        emailLabel.setBounds(350, 70, 50, 30);
        emailLabel.setFont(new Font("Arial", Font.BOLD, 15));
        logFrame.add(emailLabel);

        JLabel passLabel = new JLabel("Password");
        passLabel.setBounds(350, 150, 100, 30);
        passLabel.setFont(new Font("Arial", Font.BOLD, 15));
        logFrame.add(passLabel);

        // textfield
        emailFielLogin = new JTextField();
        emailFielLogin.setBounds(350, 100, 300, 50);
        logFrame.add(emailFielLogin);

        passwordFieldLogin = new JPasswordField();
        passwordFieldLogin.setBounds(350, 180, 300, 50);
        logFrame.add(passwordFieldLogin);

        // button
        JButton loginButton = new JButton("Login");
        loginButton.setBounds(550, 250, 100, 30);
        loginButton.addActionListener(e -> finishLogin(logFrame, mainframe));
        logFrame.add(loginButton);

        logFrame.setVisible(true);
    }

    public static void finishLogin(JFrame logFrame, JFrame mainframe){

        String username = emailFielLogin.getText();
        String passwordLogin = new String(passwordFieldLogin.getPassword());

        if(username.isEmpty()||passwordLogin.isEmpty()){
            JOptionPane.showMessageDialog(null, "All fields are required!", "Information Massage", JOptionPane.ERROR_MESSAGE);
            return;
        }

        for(int i=0; i < CountAccount; i++){
            if(allAccounts[i].getEmail().equals(username) && allAccounts[i].getPassword().equals(passwordLogin)){
                Account account = allAccounts[i];
                JOptionPane.showMessageDialog(null, "Successfully Login!", "Information Massage", JOptionPane.INFORMATION_MESSAGE);
                logFrame.dispose();
                studentDashboard(account, mainframe);
                return;
            }   
        }

        JOptionPane.showMessageDialog(null, "Account not exist!", "Information Massage", JOptionPane.ERROR_MESSAGE);
    }

    public static void studentDashboard(Account account, JFrame mainframe){
        mainframe.dispose();

        JFrame studentDashboardFrame = new JFrame("Student Dashboard");
        studentDashboardFrame.setSize(1000, 600);
        studentDashboardFrame.setResizable(false);
        studentDashboardFrame.setLayout(null);

        ImageIcon imageicon = new ImageIcon("image.PNG");
        Image Image = imageicon.getImage();
        Image newimage = Image.getScaledInstance(500, 500, java.awt.Image.SCALE_SMOOTH);
        imageicon = new ImageIcon(newimage);
        studentDashboardFrame.setIconImage(imageicon.getImage());

        JLabel imagLabel = new JLabel();
        imagLabel.setIcon(imageicon);
        imagLabel.setFont(new Font("Arial", Font.BOLD, 16));
        studentDashboardFrame.add(imagLabel);

        JPanel imagepanel = new JPanel();
        imagepanel.setBackground(Color.lightGray);
        imagepanel.setBounds(0, 0, 500, 600);
        studentDashboardFrame.add(imagepanel);
        imagepanel.add(imagLabel);

        // label
        JLabel WelcomeLabel = new JLabel("Student Dashboard", SwingConstants.CENTER);
        WelcomeLabel.setBounds(600, 10,300 ,40);
        WelcomeLabel.setFont(new Font("Arial", Font.BOLD, 16));
        studentDashboardFrame.add(WelcomeLabel);

        // button
        JButton homeButton = new JButton("Home page");
        homeButton.setBounds(650, 50, 200, 60);
        homeButton.addActionListener(e->homePageScreen(account, studentDashboardFrame, mainframe));
        studentDashboardFrame.add(homeButton);

        JButton securityButton = new JButton("Security");
        securityButton.setBounds(650, 150, 200, 60);
        securityButton.addActionListener(e->securityscreen(account, studentDashboardFrame, mainframe));
        studentDashboardFrame.add(securityButton);

        JButton updateButton = new JButton("Update");
        updateButton.setBounds(650, 250, 200, 60);
        updateButton.addActionListener(e->updateScreen(account, studentDashboardFrame, mainframe));
        studentDashboardFrame.add(updateButton);

        JButton deleteButton = new JButton("Delete Account");
        deleteButton.setBounds(650, 350, 200, 60);
        deleteButton.addActionListener(e->deleteScreen(account, studentDashboardFrame, mainframe));
        studentDashboardFrame.add(deleteButton);

        JButton logoutButton = new JButton("Logout");
        logoutButton.setBounds(650, 450, 200, 60);
        logoutButton.addActionListener(e->{
            studentDashboardFrame.dispose();
            main(null);
        });
        studentDashboardFrame.add(logoutButton);

        studentDashboardFrame.setVisible(true);
    }

    public static void homePageScreen(Account account, JFrame studentDashboardFrame, JFrame mainframe){
        studentDashboardFrame.dispose();

        JFrame homePageFrame = new JFrame("Home Page");
        homePageFrame.setSize(1000, 600);
        homePageFrame.setResizable(false);
        homePageFrame.setLayout(new GridLayout(11, 2));

        JButton cancelButton = new JButton("Cancel");
        cancelButton.addActionListener(e->{
            studentDashboard(account, mainframe);
            homePageFrame.dispose();
        });

        // label
        homePageFrame.add(new JLabel("Name: "));
        homePageFrame.add(new JLabel(account.getName()));
        homePageFrame.add(new JLabel("Age: "));
        homePageFrame.add(new JLabel(account.getAge()));
        homePageFrame.add(new JLabel("Phone Number: "));
        homePageFrame.add(new JLabel(account.getPhoneNumber()));
        homePageFrame.add(new JLabel("Gender: "));
        homePageFrame.add(new JLabel(account.getGender()));
        homePageFrame.add(new JLabel("Section: "));
        homePageFrame.add(new JLabel(account.getSection()));
        homePageFrame.add(new JLabel("Course: "));
        homePageFrame.add(new JLabel(account.getcourse()));
        homePageFrame.add(new JLabel("Year Level: "));
        homePageFrame.add(new JLabel(account.getyearLevel()));
        homePageFrame.add(new JLabel("Email: "));
        homePageFrame.add(new JLabel(account.getEmail()));
        homePageFrame.add(new JLabel("Password: "));
        homePageFrame.add(new JLabel(account.getPassword()));
        homePageFrame.add(new JLabel("Student ID: "));
        homePageFrame.add(new JLabel(account.getID()));
        homePageFrame.add(new JLabel());
        homePageFrame.add(cancelButton);

        homePageFrame.setVisible(true);
    }

    public static void securityscreen(Account account, JFrame studentDashboardFrame, JFrame mainframe){
        studentDashboardFrame.dispose();
        JFrame securityFrame = new JFrame("security");
        securityFrame.setSize(1000, 300);
        securityFrame.setResizable(false);
        securityFrame.setLayout(new GridLayout(6, 2,5 ,5));

        // textfield 
        JTextField newPasswordfField = new JTextField();

        // cancel
        JButton cancelButton = new JButton("Cancel");
        cancelButton.addActionListener(e->{
            studentDashboard(account, mainframe);
            securityFrame.dispose();
        });
        
        // submit
        JButton submitButton = new JButton("Submit");
        submitButton.addActionListener(e->{
            String newPassword = newPasswordfField.getText();
            if(!newPassword.isEmpty()){
                account.setPassword(newPassword);
                securityFrame.dispose();
                JOptionPane.showMessageDialog(null, "Password successfully changed!", "Information Massage", JOptionPane.INFORMATION_MESSAGE);
                System.out.println("Password successfully changed!");
                studentDashboard(account, mainframe);
            }else{
                JOptionPane.showMessageDialog(null, "You need to fill this out!", "Information Massage", JOptionPane.ERROR_MESSAGE);
            }
        });
        
        securityFrame.add(new JLabel());
        securityFrame.add(new JLabel());
        securityFrame.add(new JLabel("Current Password: "));
        securityFrame.add(new JLabel(account.getPassword()));
        securityFrame.add(new JLabel("Create a new Password: "));
        securityFrame.add(newPasswordfField);
        securityFrame.add(cancelButton);
        securityFrame.add(submitButton);
        securityFrame.add(new JLabel());
        
        securityFrame.setVisible(true);
    }

    public static void updateScreen(Account account, JFrame studentDashboardFrame, JFrame mainframe){
        studentDashboardFrame.dispose();
        JFrame updateFrame = new JFrame("Update");
        updateFrame.setSize(1000, 600);
        updateFrame.setResizable(false);
        updateFrame.setLayout(new GridLayout(9, 2));

        newgenderBox = new JComboBox<>(gender);
        newsecBox = new JComboBox<>(sections);
        newcourseBox = new JComboBox<>(courses);
        
        // textfield
        JTextField newnameField = new JTextField(account.getName());
        JTextField newageField = new JTextField(account.getAge());
        JTextField newphonenumberField = new JTextField(account.getPhoneNumber());
        JTextField newyearLevelField = new JTextField(account.getyearLevel());
        JTextField newemailField = new JTextField(account.getEmail());
        
        // cancelbutton
        JButton cancelButton = new JButton("Cancel");
        cancelButton.addActionListener(e->{
            studentDashboard(account, mainframe);
            updateFrame.dispose();
        });

        // submitButton
        JButton submitButton = new JButton("Submit");
        submitButton.addActionListener(e->{
            String newgender = (String)newgenderBox.getSelectedItem();
            String newsection = (String)newsecBox.getSelectedItem();
            String newcourse = (String)newcourseBox.getSelectedItem();


            String newname = newnameField.getText();
            String newage = newageField.getText();
            String newphonenumber = newphonenumberField.getText();
            String newyearLevel = newyearLevelField.getText();
            String newemail = newemailField.getText();
            

            if(!newname.isEmpty() && !newage.isEmpty() && !newphonenumber.isEmpty() && !newemail.isEmpty() && !newyearLevel.isEmpty()){
                account.setName(newname);
                account.setAge(newage);
                account.setPhoneNumber(newphonenumber);
                account.setEmail(newemail);
                account.setyearLevel(newyearLevel);

                account.setGender(newgender);
                account.setSection(newsection);
                account.setCourse(newcourse);

                JOptionPane.showMessageDialog(null, "Your account has been successfully updated!", "Information Massage", JOptionPane.INFORMATION_MESSAGE);
                System.out.println("Your account has been successfully updated!\n"+ account);
                studentDashboardFrame.dispose();
                updateFrame.dispose();
                studentDashboard(account, mainframe);
            }else{
                JOptionPane.showMessageDialog(null, "All fields are required!", "Information Massage", JOptionPane.ERROR_MESSAGE);
            }
        });

        // frame gridlayout
        updateFrame.add(new JLabel("Full Name:"));
        updateFrame.add(newnameField);
        updateFrame.add(new JLabel("Age"));
        updateFrame.add(newageField);
        updateFrame.add(new JLabel("Phone Number:"));
        updateFrame.add(newphonenumberField);
        updateFrame.add(new JLabel("Gender:"));
        updateFrame.add(newgenderBox);
        updateFrame.add(new JLabel("Section:"));
        updateFrame.add(newsecBox);
        updateFrame.add(new JLabel("Course:"));
        updateFrame.add(newcourseBox);
        updateFrame.add(new JLabel("Year Level:"));
        updateFrame.add(newyearLevelField);
        updateFrame.add(new JLabel("Email: "));
        updateFrame.add(newemailField);
        updateFrame.add(cancelButton);
        updateFrame.add(submitButton);

        updateFrame.setVisible(true);
    }

    public static void deleteScreen(Account account, JFrame studentDashboard, JFrame mainframe){
        
        studentDashboard.dispose();
        JFrame deleteAccountFrame = new JFrame("Delete Account");
        deleteAccountFrame.setSize(1000, 300);
        deleteAccountFrame.setResizable(false);
        deleteAccountFrame.setLayout(null);
    
        // Label
        JLabel label = new JLabel("This will permanently delete your account.");
        label.setBounds(300, 50, 400, 40);
        label.setFont(new Font("Arial", Font.BOLD, 16));
        label.setForeground(Color.red);
        deleteAccountFrame.add(label);
    
        // button
        JButton deleteButton = new JButton(" Delete Account ");
        deleteButton.setBounds(550, 100, 150, 35);
        deleteButton.addActionListener(e->{
            int answer = JOptionPane.showConfirmDialog(null, "You want to delete your account?", "Delete Account", JOptionPane.YES_NO_OPTION);
            if(answer == 0){
                for(int i=0; i < CountAccount; i++){
                    if(allAccounts[i].getEmail().equals(account.getEmail())){
                        allAccounts[i] = allAccounts[CountAccount - 1];
                        CountAccount--;
                    break;
                    }
                }
                studentDashboard.dispose();
                deleteAccountFrame.dispose();
                System.out.println("Account is Successfully Delete!");
                main(null);
                JOptionPane.showMessageDialog(null, "Account Successfully Deleted!", "Information Massage", JOptionPane.INFORMATION_MESSAGE);
            }else{
                System.out.println("Delete Account Cancel!");
            }
        });
        deleteAccountFrame.add(deleteButton);

        // cancelButton
        JButton cancelbutton = new JButton("Cancel");
        cancelbutton.setBounds(200, 100, 150, 35);
        cancelbutton.addActionListener(e->{
            studentDashboard(account, mainframe);
            deleteAccountFrame.dispose();
        });
        deleteAccountFrame.add(cancelbutton);

        deleteAccountFrame.setVisible(true);
    }

    public static class Account {
        String name;
        String age;
        String phoneNumber;
        String gender;
        String section;
        String course;
        String yearLevel;
        String email;
        String password;
        String ID;

        public Account(String name, String age, String phoneNumber, String gender, String section, String course, String yearLevel, String email, String password, String ID) {
            this.name = name;
            this.age = age;
            this.phoneNumber = phoneNumber;
            this.gender = gender;
            this.section = section;
            this.course = course;
            this.yearLevel = yearLevel;
            this.email = email;
            this.password = password;
            this.ID =ID;
        }

        public String getName() {
            return name;
        }

        public String getAge() {
            return age;
        }

        public String getPhoneNumber() {
            return phoneNumber;
        }

        public String getGender(){
            return gender;
        }

        public String getSection() {
            return section;
        }

        public String getcourse() {
            return course;
        }

        public String getyearLevel(){
            return yearLevel;
        }

        public String getEmail(){
            return email;
        }

        public String getPassword(){
            return password;
        }

        public String getID(){
            return ID;
        }

        public String setPassword(String newPassword){
            return this.password = newPassword;
        }

        public String setName(String newname){
            return this.name = newname;
        }

        public String setAge(String newage){
            return this.age = newage;
        }

        public String setPhoneNumber(String newphonenumber){
            return this.phoneNumber = newphonenumber;
        }

        public String setGender(String newgender){
            return this.gender = newgender;
        }

        public String setSection(String newsection){
            return this.section = newsection;
        }

        public String setCourse(String newcourse){
            return this.course = newcourse;
        }

        public String setyearLevel(String newyearLevel){
            return this.yearLevel = newyearLevel;
        }

        public String setEmail(String newemail){
            return this.email = newemail;
        }

        public String toString() {
            return "Account{" +
                    "name='" + name + '\'' +
                    ", Age='" + age + '\'' +
                    ", phoneNumber='" + phoneNumber + '\'' +
                    ", Gender=" + gender + '\'' +
                    ", Section='" + section + '\'' +
                    ", course=" + course + '\'' +
                    ", Year Level=" + yearLevel + '\'' + 
                    ", Email=" + email + '\'' +
                    ", Password=" + password + '\'' +
                    ", Student ID=" +ID +
                    '}';
        }
    }
}