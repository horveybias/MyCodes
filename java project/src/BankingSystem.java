import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

public class BankingSystem {
    public static JFrame mainFrame;
    public static ArrayList<Account> allAccounts = new ArrayList<>();
    public static JTextField nameField, addressField, phoneField, pinField, balanceField;
    public static JTextField usernameField, passwordField;

    public static void main(String[] args){
        
        mainFrame = new JFrame("BANKING SYSTEM");
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainFrame.setResizable(false);
        mainFrame.setSize(400, 300);
        mainFrame.setLayout(null);

        JLabel welcomeLabel = new JLabel("Welcome to Banking System", SwingConstants.CENTER);
        welcomeLabel.setBounds(0, 30, 400, 30);
        welcomeLabel.setFont(new Font("Arial", Font.BOLD, 16));
        mainFrame.add(welcomeLabel);

        JButton registerButton = new JButton("Register Account");
        registerButton.setBounds(100, 100, 200, 40);
        registerButton.addActionListener(e -> register());
        mainFrame.add(registerButton);

        JButton loginButton = new JButton("Log In Account");
        loginButton.setBounds(100, 150, 200, 40);
        loginButton.addActionListener(e -> logIn());
        mainFrame.add(loginButton);

        JButton exitButton = new JButton("Exit Program");
        exitButton.setBounds(100, 200, 200, 40);
        exitButton.addActionListener(e -> System.exit(0));
        mainFrame.add(exitButton);

        mainFrame.setVisible(true);
    
    }

    public static void register() {
        JFrame registerFrame = new JFrame("Register");
        registerFrame.setSize(400, 300);
        registerFrame.setResizable(false);
        registerFrame.setLayout(new GridLayout(7, 2,0,10));

        nameField = new JTextField();
        addressField = new JTextField();
        phoneField = new JTextField();
        pinField = new JTextField();
        balanceField = new JTextField();

        registerFrame.add(new JLabel("Name: "));
        registerFrame.add(nameField);
        registerFrame.add(new JLabel("Address: "));
        registerFrame.add(addressField);
        registerFrame.add(new JLabel("Phone Number: "));
        registerFrame.add(phoneField);
        registerFrame.add(new JLabel("PIN: "));
        registerFrame.add(pinField);
        registerFrame.add(new JLabel("Balance: "));
        registerFrame.add(balanceField);
        registerFrame.add(new JLabel(""));

        JButton registerButton = new JButton("Register");
        registerButton.addActionListener(e -> finishRegister(registerFrame));
        registerFrame.add(registerButton);

        registerFrame.setVisible(true);
    }

    public static void finishRegister(JFrame registerFrame) {
        String name = nameField.getText();
        String address = addressField.getText();
        String phoneNumber = phoneField.getText();
        String pin = pinField.getText();
        String balanceText = balanceField.getText();
        
        if (name.isEmpty() || address.isEmpty() || phoneNumber.isEmpty() || pin.isEmpty() || balanceText.isEmpty()) {
            JOptionPane.showMessageDialog(null, "All fields are required!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
            return;
        }

        try {
            int balance = Integer.parseInt(balanceText);
            for (Account account : allAccounts) {
                if (account.getName().equals(name)) {
                    JOptionPane.showMessageDialog(null, "Account already exists!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                if (account.getPin().equals(pin)) {
                    JOptionPane.showMessageDialog(null, "Account already exists!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
                    return;
                }
            }

            Account newAccount = new Account(name, address, phoneNumber, pin, balance);
            allAccounts.add(newAccount);
            System.out.println(newAccount);
            registerFrame.dispose();
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(null, "Invalid balance amount!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void logIn() {
        JFrame loginFrame = new JFrame("Log In");
        loginFrame.setSize(400, 200);
        loginFrame.setResizable(false);
        loginFrame.setLayout(new GridLayout(4, 2,0,10));

        usernameField = new JTextField();
        passwordField = new JTextField();

        loginFrame.add(new JLabel("Username: "));
        loginFrame.add(usernameField);
        loginFrame.add(new JLabel("Password: "));
        loginFrame.add(passwordField);
        loginFrame.add(new JLabel(""));

        JButton loginButton = new JButton("Log In");
        loginButton.addActionListener(e -> logInSession(loginFrame));
        loginFrame.add(loginButton);

        loginFrame.setVisible(true);
    }

    public static void logInSession(JFrame loginFrame) {
        String username = usernameField.getText();
        String password = passwordField.getText();

        if (username.isEmpty() || password.isEmpty()) {
            JOptionPane.showMessageDialog(null, "All fields are required!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
            return;
        }

        for (Account account : allAccounts) {
            if (account.getName().equals(username) && account.getPin().equals(password)) {
                JOptionPane.showMessageDialog(null, "Successfully logged in", "Infomation Massage", JOptionPane.INFORMATION_MESSAGE);
                loginFrame.dispose();
                accountDashboard(account);
                return;
            }
        }
        JOptionPane.showMessageDialog(null, "Invalid username or password", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
        
    }

    public static void accountDashboard(Account account) {
        JFrame dashboardFrame = new JFrame("Account Dashboard");
        dashboardFrame.setSize(400, 300);
        dashboardFrame.setResizable(false);
        dashboardFrame.setLayout(new GridLayout(6, 1));

        dashboardFrame.add(new JLabel("Hello! " + account.getName(), SwingConstants.CENTER));
        dashboardFrame.add(new JLabel("Account Balance: " + account.getBalance(), SwingConstants.CENTER));

        JButton personalDetailsButton = new JButton("Personal Details");
        personalDetailsButton.addActionListener(e -> showPersonalDetails(account));
        dashboardFrame.add(personalDetailsButton);

        JButton withdrawButton = new JButton("Withdraw");
        withdrawButton.addActionListener(e -> withdraw(account));
        dashboardFrame.add(withdrawButton);

        JButton depositButton = new JButton("Deposit");
        depositButton.addActionListener(e -> deposit(account));
        dashboardFrame.add(depositButton);

        dashboardFrame.setVisible(true);
    }

    public static void showPersonalDetails(Account account) {
        JFrame personalDetailsFrame = new JFrame("Personal Details");
        personalDetailsFrame.setSize(400, 300);
        personalDetailsFrame.setResizable(false);
        personalDetailsFrame.setLayout(new GridLayout(5, 2));

        personalDetailsFrame.add(new JLabel("Name: "));
        personalDetailsFrame.add(new JLabel(account.getName()));
        personalDetailsFrame.add(new JLabel("Address: "));
        personalDetailsFrame.add(new JLabel(account.getAddress()));
        personalDetailsFrame.add(new JLabel("Phone Number: "));
        personalDetailsFrame.add(new JLabel(account.getPhoneNumber()));
        personalDetailsFrame.add(new JLabel("PIN: "));
        personalDetailsFrame.add(new JLabel(account.getPin()));
        personalDetailsFrame.add(new JLabel("Balance: "));
        personalDetailsFrame.add(new JLabel(String.valueOf(account.getBalance())));

        personalDetailsFrame.setVisible(true);
    }

    public static void withdraw(Account account) {
        JFrame withdrawFrame = new JFrame("Withdraw");
        withdrawFrame.setSize(400, 200);
        withdrawFrame.setResizable(false);
        withdrawFrame.setLayout(null);

        JTextField amountField = new JTextField();
        amountField.setBounds(100, 0, 200, 30);

        JLabel amountlabel = new JLabel("Amount: ");
        amountlabel.setBounds(0, 0, 100, 30);

        withdrawFrame.add(amountlabel);
        withdrawFrame.add(amountField);

        JButton withdrawButton = new JButton("Withdraw");
        withdrawButton.setBounds(100, 50, 200, 30);
        withdrawButton.addActionListener(e -> {
            try {
                int amount = Integer.parseInt(amountField.getText());
                if (amount <= 0) {
                    JOptionPane.showMessageDialog(null, "Amount must be greater than 0", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
                } else if (account.getBalance() < amount) {
                    JOptionPane.showMessageDialog(null, "Insufficient funds", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
                } else {
                    account.setBalance(account.getBalance() - amount);
                    JOptionPane.showMessageDialog(null, "Successfully withdrawn!", "Infomation Massage", JOptionPane.INFORMATION_MESSAGE);
                    withdrawFrame.dispose();
                    accountDashboard(account); 
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(null, "Invalid amount!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
            }
        });
        withdrawFrame.add(withdrawButton);
        withdrawFrame.setVisible(true);
    }

    public static void deposit(Account account) {
        JFrame depositFrame = new JFrame("Deposit");
        depositFrame.setSize(400, 200);
        depositFrame.setLayout(null);
        depositFrame.setResizable(false);

        JTextField amountField = new JTextField();
        amountField.setBounds(100, 0, 200, 30);

        JLabel amountlabel = new JLabel("Amount: ");
        amountlabel.setBounds(0, 0, 100, 30);

        depositFrame.add(amountlabel);
        depositFrame.add(amountField);

        JButton depositButton = new JButton("Deposit");
        depositButton.setBounds(100, 50, 200, 30);
        depositButton.addActionListener(e -> {
            try {
                int amount = Integer.parseInt(amountField.getText());
                if (amount <= 0) {
                    JOptionPane.showMessageDialog(null, "Amount must be greater than 0", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
                } else {
                    account.setBalance(account.getBalance() + amount);
                    JOptionPane.showMessageDialog(null, "Successfully deposited!", "Infomation Massage", JOptionPane.INFORMATION_MESSAGE);
                    depositFrame.dispose();
                    accountDashboard(account); // Refresh dashboard to show updated balance
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(null, "Invalid amount!", "Infomation Massage", JOptionPane.ERROR_MESSAGE);
            }
        });
        depositFrame.add(depositButton);
        depositFrame.setVisible(true);
    }

    public static class Account {
        String name;
        String address;
        String phoneNumber;
        String pin;
        int balance;

        public Account(String name, String address, String phoneNumber, String pin, int balance) {
            this.name = name;
            this.address = address;
            this.phoneNumber = phoneNumber;
            this.pin = pin;
            this.balance = balance;
        }

        public String getName() {
            return name;
        }

        public String getAddress() {
            return address;
        }

        public String getPhoneNumber() {
            return phoneNumber;
        }

        public String getPin() {
            return pin;
        }

        public int getBalance() {
            return balance;
        }

        public void setBalance(int balance) {
            this.balance = balance;
        }

        public String toString() {
            return "Account{" +
                    "name='" + name + '\'' +
                    ", address='" + address + '\'' +
                    ", phoneNumber='" + phoneNumber + '\'' +
                    ", pin='" + pin + '\'' +
                    ", balance=" + balance +
                    '}';
        }
    }
}