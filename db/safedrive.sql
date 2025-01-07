-- MySQL Script with proper table dropping and ordering
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
SET FOREIGN_KEY_CHECKS = 0;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_db`
--

-- Drop tables in reverse order of dependencies
DROP TABLE IF EXISTS `van`;
DROP TABLE IF EXISTS `truck`;
DROP TABLE IF EXISTS `suv`;
DROP TABLE IF EXISTS `sedan`;
DROP TABLE IF EXISTS `motorcycle`;
DROP TABLE IF EXISTS `vehicle`;
DROP TABLE IF EXISTS `thirdpartycoverage`;
DROP TABLE IF EXISTS `personal`;
DROP TABLE IF EXISTS `comprehensivecoverage`;
DROP TABLE IF EXISTS `commercial`;
DROP TABLE IF EXISTS `activepolicy`;
DROP TABLE IF EXISTS `application`;
DROP TABLE IF EXISTS `insurancepolicy`;
DROP TABLE IF EXISTS `policyholder`;

-- Create tables in order of dependencies
CREATE TABLE `policyholder` (
  `Policyholder_ID` int(11) NOT NULL,
  `Policyholder_Name` varchar(255) DEFAULT NULL,
  `Policyholder_Contact_Number` varchar(15) DEFAULT NULL,
  `Policyholder_Email` varchar(255) DEFAULT NULL,
  `Policyholder_Date_Of_Birth` date DEFAULT NULL,
  `Policyholder_Driving_License_Number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Policyholder_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `insurancepolicy` (
  `Policy_ID` int(11) NOT NULL,
  `Policy_Number` varchar(50) DEFAULT NULL,
  `Policy_Type` varchar(50) DEFAULT NULL,
  `Policy_Premium_Amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Policy_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `application` (
  `Application_ID` int(11) NOT NULL,
  `Application_Date` date DEFAULT NULL,
  `Application_Status` varchar(50) DEFAULT NULL,
  `Application_Purpose` varchar(50) DEFAULT NULL,
  `Policyholder_ID` int(11) DEFAULT NULL,
  `Policy_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`Application_ID`),
  FOREIGN KEY (`Policyholder_ID`) REFERENCES `policyholder` (`Policyholder_ID`),
  FOREIGN KEY (`Policy_ID`) REFERENCES `insurancepolicy` (`Policy_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `activepolicy` (
  `Active_Policy_ID` int(11) NOT NULL,
  `Policy_Start_Date` date DEFAULT NULL,
  `Policy_End_Date` date DEFAULT NULL,
  `Policy_ID` int(11) DEFAULT NULL,
  `Application_ID` int(11) DEFAULT NULL,
  `Policyholder_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`Active_Policy_ID`),
  FOREIGN KEY (`Policy_ID`) REFERENCES `insurancepolicy` (`Policy_ID`),
  FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`),
  FOREIGN KEY (`Policyholder_ID`) REFERENCES `policyholder` (`Policyholder_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `commercial` (
  `Application_ID` int(11) NOT NULL,
  `Fleet_Size` int(11) DEFAULT NULL,
  `Goods_Covered` varchar(255) DEFAULT NULL,
  `Business_Use_Type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Application_ID`),
  FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `comprehensivecoverage` (
  `Policy_ID` int(11) NOT NULL,
  `Repair_Coverage_Limit` int(11) DEFAULT NULL,
  `Roadside_Assistance_Included` tinyint(1) DEFAULT NULL,
  `Theft_Coverage` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Policy_ID`),
  FOREIGN KEY (`Policy_ID`) REFERENCES `insurancepolicy` (`Policy_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `personal` (
  `Application_ID` int(11) NOT NULL,
  `Mileage_Limit` int(11) DEFAULT NULL,
  `Driver_Count` int(11) DEFAULT NULL,
  PRIMARY KEY (`Application_ID`),
  FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `vehicle` (
  `Vehicle_ID` int(11) NOT NULL,
  `Vehicle_Plate_Num` varchar(20) DEFAULT NULL,
  `Vehicle_Type` varchar(50) DEFAULT NULL,
  `Vehicle_Manufacture_Year` int(11) DEFAULT NULL,
  `Policyholder_ID` int(11) DEFAULT NULL,
  `Application_ID` int(11) DEFAULT NULL,
  `Active_Policy_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  FOREIGN KEY (`Policyholder_ID`) REFERENCES `policyholder` (`Policyholder_ID`),
  FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`),
  FOREIGN KEY (`Active_Policy_ID`) REFERENCES `activepolicy` (`Active_Policy_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `motorcycle` (
  `Vehicle_ID` int(11) NOT NULL,
  `Engine_Displacement` int(11) DEFAULT NULL,
  `Helmet_Storage` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `sedan` (
  `Vehicle_ID` int(11) NOT NULL,
  `Truck_Size` int(11) DEFAULT NULL,
  `Fuel_Efficiency` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `suv` (
  `Vehicle_ID` int(11) NOT NULL,
  `Towing_Capacity` int(11) DEFAULT NULL,
  `All_Wheel_Vehicle` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `thirdpartycoverage` (
  `Policy_ID` int(11) NOT NULL,
  `Liability_Coverage_Limit` int(11) DEFAULT NULL,
  `Property_Damage_Liability` int(11) DEFAULT NULL,
  `Injury_Liability_Coverage` int(11) DEFAULT NULL,
  PRIMARY KEY (`Policy_ID`),
  FOREIGN KEY (`Policy_ID`) REFERENCES `insurancepolicy` (`Policy_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `truck` (
  `Vehicle_ID` int(11) NOT NULL,
  `Engine_Displacement` int(11) DEFAULT NULL,
  `Helmet_Storage` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `van` (
  `Vehicle_ID` int(11) NOT NULL,
  `Seating_Capacity` int(11) DEFAULT NULL,
  `Cargo_Space` int(11) DEFAULT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert data in proper order
INSERT INTO `policyholder` (`Policyholder_ID`, `Policyholder_Name`, `Policyholder_Contact_Number`, `Policyholder_Email`, `Policyholder_Date_Of_Birth`, `Policyholder_Driving_License_Number`) VALUES
(1, 'John Doe', '1234567890', 'johndoe@example.com', '1990-01-15', 'DL123456789'),
(2, 'Jane Smith', '0987654321', 'janesmith@example.com', '1985-06-22', 'DL987654321'),
(3, 'Alice Johnson', '5551234567', 'alice.johnson@example.com', '1980-03-15', 'DL987650321'),
(4, 'Bob Brown', '5559876543', 'bob.brown@example.com', '1975-11-20', 'DL123450987'),
(5, 'Charlie Green', '5555678901', 'charlie.green@example.com', '1992-07-05', 'DL567890123');

INSERT INTO `insurancepolicy` (`Policy_ID`, `Policy_Number`, `Policy_Type`, `Policy_Premium_Amount`) VALUES
(1, 'POL12345', 'Comprehensive', 1200.50),
(2, 'POL67890', 'Third Party', 850.75),
(3, 'POL11223', 'Comprehensive', 1500.00),
(4, 'POL44556', 'Third Party', 950.25),
(5, 'POL77889', 'Comprehensive', 1750.50);

INSERT INTO `application` (`Application_ID`, `Application_Date`, `Application_Status`, `Application_Purpose`, `Policyholder_ID`, `Policy_ID`) VALUES
(1, '2024-01-10', 'Approved', 'Personal', 1, 1),
(2, '2024-01-12', 'Pending', 'Commercial', 2, 2),
(3, '2024-01-15', 'Approved', 'Personal', 3, 3),
(4, '2024-01-18', 'Rejected', 'Commercial', 4, 4),
(5, '2024-01-20', 'Pending', 'Commercial', 5, 5);

INSERT INTO `activepolicy` (`Active_Policy_ID`, `Policy_Start_Date`, `Policy_End_Date`, `Policy_ID`, `Application_ID`, `Policyholder_ID`) VALUES
(1, '2024-02-01', '2025-01-31', 1, 1, 1),
(2, '2024-02-15', '2025-02-14', 2, 2, 2),
(3, '2024-03-01', '2025-02-28', 3, 3, 3),
(4, '2024-04-01', '2025-03-31', 4, 4, 4),
(5, '2024-05-01', '2025-04-30', 5, 5, 5);

INSERT INTO `commercial` (`Application_ID`, `Fleet_Size`, `Goods_Covered`, `Business_Use_Type`) VALUES
(1, NULL, NULL, NULL),
(2, 5, 'Pharmaceutical Products', 'Medical Supplies Delivery'),
(3, NULL, NULL, NULL),
(4, 8, 'Electronics', 'Delivery Service'),
(5, 12, 'Construction Materials', 'Heavy Equipment Transport');

INSERT INTO `comprehensivecoverage` (`Policy_ID`, `Repair_Coverage_Limit`, `Roadside_Assistance_Included`, `Theft_Coverage`) VALUES
(1, 10000, 1, 1),
(2, NULL, NULL, NULL),
(3, 12000, 1, 1),
(4, NULL, NULL, NULL),
(5, 18000, 1, 0);

INSERT INTO `personal` (`Application_ID`, `Mileage_Limit`, `Driver_Count`) VALUES
(1, 15000, 2),
(2, NULL, NULL),
(3, 12000, 1),
(4, NULL, NULL),
(5, NULL, NULL);

INSERT INTO `thirdpartycoverage` (`Policy_ID`, `Liability_Coverage_Limit`, `Property_Damage_Liability`, `Injury_Liability_Coverage`) VALUES
(1, NULL, NULL, NULL),
(2, 500000, 100000, 300000),
(3, NULL, NULL, NULL),
(4, 800000, 250000, 450000),
(5, NULL, NULL, NULL);

INSERT INTO `vehicle` (`Vehicle_ID`, `Vehicle_Plate_Num`, `Vehicle_Type`, `Vehicle_Manufacture_Year`, `Policyholder_ID`, `Application_ID`, `Active_Policy_ID`) VALUES
(1, 'ABC123', 'Sedan', 2018, 1, 1, 1),
(2, 'XYZ789', 'Truck', 2020, 2, 2, 2),
(3, 'LMN456', 'SUV', 2022, 3, 3, 3),
(4, 'OPQ123', 'Van', 2021, 4, 4, 4),
(5, 'RST890', 'Motorcycle', 2020, 5, 5, 5);

INSERT INTO `motorcycle` (`Vehicle_ID`, `Engine_Displacement`, `Helmet_Storage`) VALUES
(5, 749, 1);

INSERT INTO `sedan` (`Vehicle_ID`, `Truck_Size`, `Fuel_Efficiency`) VALUES
(1, 15, 25.50);

INSERT INTO `suv` (`Vehicle_ID`, `Towing_Capacity`, `All_Wheel_Vehicle`) VALUES
(3, 5000, 1);

INSERT INTO `truck` (`Vehicle_ID`, `Engine_Displacement`, `Helmet_Storage`) VALUES
(5, 749, 1);

INSERT INTO `van` (`Vehicle_ID`, `Seating_Capacity`, `Cargo_Space`) VALUES
(4, 8, 145);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;