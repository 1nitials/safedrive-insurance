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

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 07, 2025 at 03:49 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_database`
--

-- Drop tables in reverse order of dependencies
DROP TABLE IF EXISTS `van`;
DROP TABLE IF EXISTS `truck`;
DROP TABLE IF EXISTS `suv`;
DROP TABLE IF EXISTS `sedan`;
DROP TABLE IF EXISTS `motorcycle`;
DROP TABLE IF EXISTS `vehicle`;
DROP TABLE IF EXISTS `third_party_coverage`;
DROP TABLE IF EXISTS `personal`;
DROP TABLE IF EXISTS `comprehensive_coverage`;
DROP TABLE IF EXISTS `commercial`;
DROP TABLE IF EXISTS `active_policy`;
DROP TABLE IF EXISTS `application`;
DROP TABLE IF EXISTS `insurance_policy`;
DROP TABLE IF EXISTS `policyholder`;

-- --------------------------------------------------------

--
-- Table structure for table `active_policy`
--

CREATE TABLE `active_policy` (
  `Active_Policy_ID` int(11) NOT NULL,
  `Policy_Start_Date` date NOT NULL,
  `Policy_End_Date` date NOT NULL,
  `Application_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `active_policy`
--

INSERT INTO `active_policy` (`Active_Policy_ID`, `Policy_Start_Date`, `Policy_End_Date`, `Application_ID`) VALUES
(1, '2025-01-15', '2026-01-15', 1),
(2, '2025-02-01', '2026-02-01', 4),
(3, '2025-03-01', '2026-03-01', 6),
(4, '2025-03-10', '2026-03-10', 8);

-- --------------------------------------------------------

--
-- Table structure for table `application`
--

CREATE TABLE `application` (
`Application_ID` int(11) NOT NULL,
`Application_Date` date NOT NULL,
`Application_Status` enum('Pending','Approved','Rejected') NOT NULL,
`Application_Purpose` enum('PERSONAL','COMMERCIAL') NOT NULL,
`Policyholder_ID` int(11) NOT NULL,
`Policy_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application`
--

INSERT INTO `application` (`Application_ID`, `Application_Date`, `Application_Status`, `Application_Purpose`, `Policyholder_ID`, `Policy_ID`) VALUES
(1, '2025-01-01', 'Approved', 'PERSONAL', 1, 1),
(2, '2025-01-05', 'Pending', 'COMMERCIAL', 2, 2),
(3, '2025-01-10', 'Rejected', 'PERSONAL', 3, 3),
(4, '2025-01-15', 'Approved', 'COMMERCIAL', 4, 4),
(5, '2025-01-20', 'Pending', 'PERSONAL', 5, 5),
(6, '2025-01-25', 'Approved', 'PERSONAL', 6, 6),
(7, '2025-01-30', 'Rejected', 'COMMERCIAL', 7, 7),
(8, '2025-02-01', 'Approved', 'COMMERCIAL', 8, 8);

-- --------------------------------------------------------

--
-- Table structure for table `commercial`
--

CREATE TABLE `commercial` (
`Application_ID` int(11) NOT NULL,
`Fleet_Size` int(11) NOT NULL,
`Goods_Covered` varchar(255) NOT NULL,
`Business_Use_Type` enum('Delivery','Passenger Transport','Logistics','Other') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `commercial`
--

INSERT INTO `commercial` (`Application_ID`, `Fleet_Size`, `Goods_Covered`, `Business_Use_Type`) VALUES
(2, 10, 'Electronics', 'Delivery'),
(4, 15, 'Perishable Goods', 'Logistics'),
(7, 8, 'Clothing', ''),
(8, 12, 'Furniture', '');

-- --------------------------------------------------------

--
-- Table structure for table `comprehensive_coverage`
--

CREATE TABLE `comprehensive_coverage` (
`Policy_ID` int(11) NOT NULL,
`Repair_Coverage_Limit` decimal(10,2) NOT NULL,
`Roadside_Assistance_Included` tinyint(1) NOT NULL,
`Theft_Coverage` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comprehensive_coverage`
--

INSERT INTO `comprehensive_coverage` (`Policy_ID`, `Repair_Coverage_Limit`, `Roadside_Assistance_Included`, `Theft_Coverage`) VALUES
(2, 200000.00, 1, 1),
(3, 150000.00, 0, 1),
(5, 250000.00, 1, 1),
(7, 180000.00, 0, 1),
(8, 210000.00, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `insurance_policy`
--

CREATE TABLE `insurance_policy` (
`Policy_ID` int(11) NOT NULL,
`Policy_Number` varchar(20) NOT NULL,
`Policy_Type` enum('THIRD_PARTY_COVERAGE','COMPREHENSIVE_COVERAGE') NOT NULL,
`Policy_Premium_Amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `insurance_policy`
--

INSERT INTO `insurance_policy` (`Policy_ID`, `Policy_Number`, `Policy_Type`, `Policy_Premium_Amount`) VALUES
(1, 'POL123456', 'THIRD_PARTY_COVERAGE', 500.00),
(2, 'POL654321', 'COMPREHENSIVE_COVERAGE', 1200.00),
(3, 'POL987654', 'COMPREHENSIVE_COVERAGE', 1000.00),
(4, 'POL246810', 'THIRD_PARTY_COVERAGE', 600.00),
(5, 'POL135791', 'COMPREHENSIVE_COVERAGE', 1400.00),
(6, 'POL567890', 'THIRD_PARTY_COVERAGE', 550.00),
(7, 'POL432109', 'COMPREHENSIVE_COVERAGE', 1250.00),
(8, 'POL678345', 'COMPREHENSIVE_COVERAGE', 1300.00);

-- --------------------------------------------------------

--
-- Table structure for table `motorcycle`
--

CREATE TABLE `motorcycle` (
`Vehicle_ID` int(11) NOT NULL,
`Engine_Displacement` decimal(5,2) NOT NULL,
`Helmet_Storage` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `motorcycle`
--

INSERT INTO `motorcycle` (`Vehicle_ID`, `Engine_Displacement`, `Helmet_Storage`) VALUES
(4, 999.99, 1);

-- --------------------------------------------------------

--
-- Table structure for table `personal`
--

CREATE TABLE `personal` (
`Application_ID` int(11) NOT NULL,
`Mileage_Limit` decimal(8,2) NOT NULL,
`Driver_Count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personal`
--

INSERT INTO `personal` (`Application_ID`, `Mileage_Limit`, `Driver_Count`) VALUES
(1, 15000.00, 2),
(3, 20000.00, 1),
(5, 12000.00, 1),
(6, 18000.00, 3);

-- --------------------------------------------------------

--
-- Table structure for table `policyholder`
--

CREATE TABLE `policyholder` (
  `Policyholder_ID` int(11) NOT NULL,
  `Policyholder_Name` varchar(100) NOT NULL,
  `Policyholder_Contact_Number` varchar(15) NOT NULL,
  `Policyholder_Email` varchar(100) NOT NULL,
  `Policyholder_Date_Of_Birth` date NOT NULL,
  `Policyholder_Driving_License_Number` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Then, insert or reference the Policyholder_ID
INSERT INTO `policyholder` (`Policyholder_Name`, `Policyholder_Contact_Number`, `Policyholder_Email`, `Policyholder_Date_Of_Birth`, `Policyholder_Driving_License_Number`) 
VALUES ('John Doe', '0123456789', 'john.doe@example.com', '1970-01-01', 'D1234567');


--
-- Dumping data for table `policyholder`
--

INSERT INTO `policyholder` (`Policyholder_ID`, `Policyholder_Name`, `Policyholder_Contact_Number`, `Policyholder_Email`, `Policyholder_Date_Of_Birth`, `Policyholder_Driving_License_Number`) VALUES
(1, 'Izz Ezzad Syameir', '0123456789', 'izz.ezz@example.com', '2003-03-13', 'D12345678'),
(2, 'Neasthy Laade', '0198765432', 'neasthy.laade@example.com', '2004-10-22', 'D98765432'),
(3, 'Isaac', '0112233445', 'Isaac.shagal@example.com', '2004-12-05', 'D33445566'),
(4, 'Ronad', '0102203321', 'ronad.jedol@example.com', '2004-07-30', 'D49020044'),
(5, 'Ming', '01116385037', 'ming.lee@example.com', '2003-02-14', 'D39759473'),
(6, 'Ali Bin Ahmad', '0112233445', 'ali.ahmad@example.com', '1992-12-05', 'D29475374'),
(7, 'Nurul Afiqah', '0183345678', 'afiqah.hassan@example.com', '2002-01-25', 'D66554433'),
(8, 'Kumar Rajan', '0129876543', 'kumar.rajan@example.com', '1989-11-12', 'D77889900');

-- --------------------------------------------------------

--
-- Table structure for table `sedan`
--

CREATE TABLE `sedan` (
`Vehicle_ID` int(11) NOT NULL,
`Trunk_Size` decimal(5,2) NOT NULL,
`Fuel_Efficiency` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sedan`
--

INSERT INTO `sedan` (`Vehicle_ID`, `Trunk_Size`, `Fuel_Efficiency`) VALUES
(1, 450.00, 12.50),
(6, 400.00, 15.00);

-- --------------------------------------------------------

--
-- Table structure for table `suv`
--

CREATE TABLE `suv` (
`Vehicle_ID` int(11) NOT NULL,
`Towing_Capacity` decimal(6,2) NOT NULL,
`All_Wheel_Drive` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suv`
--

INSERT INTO `suv` (`Vehicle_ID`, `Towing_Capacity`, `All_Wheel_Drive`) VALUES
(2, 2000.00, 1),
(7, 2500.00, 1);

-- --------------------------------------------------------

--
-- Table structure for table `third_party_coverage`
--

CREATE TABLE `third_party_coverage` (
`Policy_ID` int(11) NOT NULL,
`Liability_Coverage_Limit` decimal(10,2) NOT NULL,
`Property_Damage_Liability` decimal(10,2) NOT NULL,
`Injury_Liability_Coverage` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `third_party_coverage`
--

INSERT INTO `third_party_coverage` (`Policy_ID`, `Liability_Coverage_Limit`, `Property_Damage_Liability`, `Injury_Liability_Coverage`) VALUES
(1, 100000.00, 50000.00, 25000.00),
(4, 120000.00, 60000.00, 30000.00),
(6, 110000.00, 55000.00, 28000.00);

-- --------------------------------------------------------

--
-- Table structure for table `truck`
--

CREATE TABLE `truck` (
`Vehicle_ID` int(11) NOT NULL,
`Payload_Capacity` decimal(6,2) NOT NULL,
`Number_Of_Tyres` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `truck`
--

INSERT INTO `truck` (`Vehicle_ID`, `Payload_Capacity`, `Number_Of_Tyres`) VALUES
(3, 5000.00, 8),
(8, 6000.00, 10);

-- --------------------------------------------------------

--
-- Table structure for table `van`
--

CREATE TABLE `van` (
`Vehicle_ID` int(11) NOT NULL,
`Seating_Capacity` int(11) NOT NULL,
`Cargo_Space` decimal(6,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `van`
--

INSERT INTO `van` (`Vehicle_ID`, `Seating_Capacity`, `Cargo_Space`) VALUES
(5, 12, 3000.00);

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `Vehicle_ID` int(11) NOT NULL,
  `Vehicle_Plate_Num` varchar(15) NOT NULL,
  `Vehicle_Type` enum('SEDAN','SUV','TRUCK','MOTORCYCLE','VAN') NOT NULL,
  `Vehicle_Manufacture_Year` year(4) NOT NULL,
  `Application_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`Vehicle_ID`, `Vehicle_Plate_Num`, `Vehicle_Type`, `Vehicle_Manufacture_Year`, `Application_ID`) VALUES
(1, 'ABC1234', 'SEDAN', '2018', 1),
(2, 'XYZ5678', 'SUV', '2020', 2),
(3, 'MNO9876', 'TRUCK', '2017', 3),
(4, 'DEF3456', 'MOTORCYCLE', '2021', 4),
(5, 'GHI7890', 'VAN', '2019', 5),
(6, 'JKL2345', 'SEDAN', '2016', 6),
(7, 'PQR1234', 'SUV', '2022', 7),
(8, 'STU6789', 'TRUCK', '2018', 8);

-- 
-- Add Indexes and Constraints to Existing Tables
--

-- Indexes for table `active_policy`
ALTER TABLE `active_policy`
ADD PRIMARY KEY (`Active_Policy_ID`),
ADD KEY `fk_active_policy_application` (`Application_ID`);

-- Indexes for table `application`
ALTER TABLE `application`
ADD PRIMARY KEY (`Application_ID`),
ADD KEY `fk_application_policyholder` (`Policyholder_ID`),
ADD KEY `fk_application_policy` (`Policy_ID`);

-- Indexes for table `commercial`
ALTER TABLE `commercial`
ADD PRIMARY KEY (`Application_ID`);

-- Indexes for table `comprehensive_coverage`
ALTER TABLE `comprehensive_coverage`
ADD PRIMARY KEY (`Policy_ID`);

-- Indexes for table `insurance_policy`
ALTER TABLE `insurance_policy`
ADD PRIMARY KEY (`Policy_ID`),
ADD UNIQUE KEY `Policy_Number` (`Policy_Number`);

-- Indexes for table `motorcycle`
ALTER TABLE `motorcycle`
ADD PRIMARY KEY (`Vehicle_ID`);

-- Indexes for table `personal`
ALTER TABLE `personal`
ADD PRIMARY KEY (`Application_ID`);

-- Indexes for table `policyholder`
ALTER TABLE `policyholder`
ADD PRIMARY KEY (`Policyholder_ID`),
ADD UNIQUE KEY `Policyholder_Email` (`Policyholder_Email`),
ADD UNIQUE KEY `Policyholder_Driving_License_Number` (`Policyholder_Driving_License_Number`);

-- Indexes for table `sedan`
ALTER TABLE `sedan`
ADD PRIMARY KEY (`Vehicle_ID`);

-- Indexes for table `suv`
ALTER TABLE `suv`
ADD PRIMARY KEY (`Vehicle_ID`);

-- Indexes for table `third_party_coverage`
ALTER TABLE `third_party_coverage`
ADD PRIMARY KEY (`Policy_ID`);

-- Indexes for table `truck`
ALTER TABLE `truck`
ADD PRIMARY KEY (`Vehicle_ID`);

-- Indexes for table `van`
ALTER TABLE `van`
ADD PRIMARY KEY (`Vehicle_ID`);

-- Indexes for table `vehicle`
ALTER TABLE `vehicle`
ADD PRIMARY KEY (`Vehicle_ID`),
ADD UNIQUE KEY `Vehicle_Plate_Num` (`Vehicle_Plate_Num`),
ADD KEY `fk_vehicle_application` (`Application_ID`);

-- 
-- Add AUTO_INCREMENT to tables
--

-- AUTO_INCREMENT for table `active_policy`
ALTER TABLE `active_policy`
MODIFY `Active_Policy_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

-- AUTO_INCREMENT for table `application`
ALTER TABLE `application`
MODIFY `Application_ID` int(11) NOT NULL AUTO_INCREMENT;

-- AUTO_INCREMENT for table `insurance_policy`
ALTER TABLE `insurance_policy`
MODIFY `Policy_ID` int(11) NOT NULL AUTO_INCREMENT;

-- AUTO_INCREMENT for table `policyholder`
ALTER TABLE `policyholder`
MODIFY `Policyholder_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

-- AUTO_INCREMENT for table `vehicle`
ALTER TABLE `vehicle`
MODIFY `Vehicle_ID` int(11) NOT NULL AUTO_INCREMENT;

-- 
-- Add Constraints for Foreign Keys
--

-- Constraints for table `active_policy`
ALTER TABLE `active_policy`
ADD CONSTRAINT `fk_active_policy_application` FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `application`
ALTER TABLE `application`
ADD CONSTRAINT `fk_application_policy` FOREIGN KEY (`Policy_ID`) REFERENCES `insurance_policy` (`Policy_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `fk_application_policyholder` FOREIGN KEY (`Policyholder_ID`) REFERENCES `policyholder` (`Policyholder_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `commercial`
ALTER TABLE `commercial`
ADD CONSTRAINT `fk_commercial_application` FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `comprehensive_coverage`
ALTER TABLE `comprehensive_coverage`
ADD CONSTRAINT `fk_comprehensive_policy` FOREIGN KEY (`Policy_ID`) REFERENCES `insurance_policy` (`Policy_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `motorcycle`
ALTER TABLE `motorcycle`
ADD CONSTRAINT `fk_motorcycle_vehicle` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `personal`
ALTER TABLE `personal`
ADD CONSTRAINT `fk_personal_application` FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `sedan`
ALTER TABLE `sedan`
ADD CONSTRAINT `fk_sedan_vehicle` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `suv`
ALTER TABLE `suv`
ADD CONSTRAINT `fk_suv_vehicle` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `third_party_coverage`
ALTER TABLE `third_party_coverage`
ADD CONSTRAINT `fk_third_party_policy` FOREIGN KEY (`Policy_ID`) REFERENCES `insurance_policy` (`Policy_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `truck`
ALTER TABLE `truck`
ADD CONSTRAINT `fk_truck_vehicle` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `van`
ALTER TABLE `van`
ADD CONSTRAINT `fk_van_vehicle` FOREIGN KEY (`Vehicle_ID`) REFERENCES `vehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `vehicle`
ALTER TABLE `vehicle`
ADD CONSTRAINT `fk_vehicle_application` FOREIGN KEY (`Application_ID`) REFERENCES `application` (`Application_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

-- No need to update the `vehicle.Application_ID` since it already connects to `application.Application_ID`.
-- Instead, ensure proper associations via joins during queries.
-- If `vehicle.Application_ID` is correctly set, there's no need for the following type of update.



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
