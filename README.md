# Teeque-backend

## Model Overview

This Django application includes custom models for handling user accounts, roles, services, orders, and reviews. The `CustomUser` model is extended from Django’s default `AbstractUser` to support email-based authentication. Additional models include `Seller`, `Buyer`, `Service`, `Order`, `OrderItem`, `Category`, `Tag`, and `Rating`, which define the core features of the platform.

Here's a table that summarizes the Django models:

| **Model**      | **Fields**                                                                                                                                          | **Relationships**                                                             | **Notes**                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **CustomUser** | `email (unique)`<br>`about`<br>`phonenumber`<br>`country`<br>`birth_date`<br>`last_login`<br>`groups`<br>`user_permissions`                         | Many-to-many with `Group` and `Permission`                                    | Custom user model using email as `USERNAME_FIELD`, with extended fields like `about` and `phonenumber`. |
| **Seller**     | `user (OneToOneField)`<br>`skills`<br>`portfolio`<br>`average_rating`<br>`number_of_reviews`                                                        | One-to-one with `CustomUser`                                                  | Automatically adds the user to the "Seller" group upon saving.                                          |
| **Buyer**      | `user (OneToOneField)`<br>`favorite_services (ManyToManyField)`                                                                                     | One-to-one with `CustomUser`<br>Many-to-many with `Service`                   | Automatically adds the user to the "Buyer" group upon saving.                                           |
| **Category**   | `name`                                                                                                                                              | N/A                                                                           | Categories for services (e.g., "Web Development").                                                      |
| **Service**    | `title`<br>`category (ForeignKey)`<br>`description`<br>`price`<br>`created_at`<br>`updated_at`<br>`seller (ForeignKey)`<br>`tags (ManyToManyField)` | ForeignKey to `Seller`<br>ForeignKey to `Category`<br>Many-to-many with `Tag` | Represents services offered by sellers.                                                                 |
| **Order**      | `created_at`<br>`buyer (ForeignKey)`                                                                                                                | ForeignKey to `Buyer`                                                         | Represents orders placed by buyers.                                                                     |
| **OrderItem**  | `order (ForeignKey)`<br>`service (ForeignKey)`<br>`order_status`                                                                                    | ForeignKey to `Order`<br>ForeignKey to `Service`                              | Tracks individual items in an order.                                                                    |
| **Tag**        | `tag (unique)`                                                                                                                                      | N/A                                                                           | Tags associated with services.                                                                          |
| **Rating**     | `service (ForeignKey)`<br>`buyer (ForeignKey)`<br>`rating`<br>`comment`<br>`created_at`                                                             | ForeignKey to `Service`<br>ForeignKey to `Buyer`                              | Represents ratings and reviews given by buyers for services.                                            |

### Key

- **One-to-one relationship:** Each `CustomUser` can be a `Seller` or a `Buyer`.
- **ForeignKey relationship:** Models like `Service`, `Order`, and `OrderItem` reference other models (e.g., `Seller`, `Category`, `Order`).
- **Many-to-many relationship:** Models like `Service` and `Buyer` can have multiple relationships through tags or favorite services.

This table provides a clear overview of the models, fields, and their relationships.

## Features

- **Custom User Authentication:** Email-based login using a custom user model.
- **Group Management:** Automatically adds users to the appropriate groups (e.g., Seller or Buyer) upon saving.
- **Service Platform:** Allows users to buy, sell, rate, and review services.
- **Order Management:** Supports order creation and status tracking.
- **Tagging and Categories:** Services can be categorized and tagged for easier browsing.

## Dependencies

- `django_countries`: For handling country fields.
- `phonenumber_field`: For handling phone numbers.
