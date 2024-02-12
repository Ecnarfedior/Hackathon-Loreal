{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "#interface bash\n",
        "#pip install pandas\n",
        "#ip install gdown"
      ],
      "metadata": {
        "id": "D3Qa63aBCwl3"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#pip install --upgrade google-colab\n",
        "#pip install gspread pandas"
      ],
      "metadata": {
        "id": "Xp6imujrCyLa"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import smtplib\n",
        "from email.mime.text import MIMEText\n",
        "from email.mime.multipart import MIMEMultipart\n",
        "from email.utils import formatdate\n",
        "import datetime\n",
        "import pytz\n",
        "import gdown\n",
        "import gspread\n",
        "import pandas as pd\n",
        "from google.colab import auth\n",
        "auth.authenticate_user()\n",
        "from google.colab import drive\n",
        "drive.mount('/content/drive')\n",
        "import nltk\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.tokenize import word_tokenize\n",
        "from nltk.probability import FreqDist"
      ],
      "metadata": {
        "id": "h4eZ3hMZx7XC",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "f164b7c2-8a78-47e7-d006-a50f759dfd02"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount(\"/content/drive\", force_remount=True).\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "nltk.download('punkt')\n",
        "nltk.download('stopwords')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ovBHvlGZran6",
        "outputId": "310b4d14-1535-460f-a1e5-9b8212e8968a"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "[nltk_data] Downloading package punkt to /root/nltk_data...\n",
            "[nltk_data]   Unzipping tokenizers/punkt.zip.\n",
            "[nltk_data] Downloading package stopwords to /root/nltk_data...\n",
            "[nltk_data]   Unzipping corpora/stopwords.zip.\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "True"
            ]
          },
          "metadata": {},
          "execution_count": 3
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# ***ENVOIS DU PREMIER MAIL A LA DATE SOUAHITES APRES LE PASSAGE D'UNE COMMANDE PAR LE CLIENT, LIEN VERS L'ENQUETE DE SATISFACTION***"
      ],
      "metadata": {
        "id": "wHmkwvSyGLZF"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "scheduled_time = '2024-01-17 10:00:00'\n",
        "scheduled_datetime = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')\n",
        "\n",
        "def send_email(to_email, subject, body, scheduled_time, sender_email, sender_password, smtp_server, smtp_port, survey_link):\n",
        "    msg = MIMEMultipart()\n",
        "    msg['From'] = sender_email\n",
        "    msg['To'] = to_email\n",
        "    msg['Subject'] = subject\n",
        "\n",
        "    # Convertir le temps programmé en format de date et heure\n",
        "    #scheduled_datetime = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')\n",
        "\n",
        "    # Récupérer le fuseau horaire local du destinataire\n",
        "    recipient_timezone = pytz.timezone('Europe/Paris')  # Remplacez 'Europe/Paris' par le fuseau horaire du destinataire\n",
        "\n",
        "    # Convertir le temps programmé au fuseau horaire local du destinataire\n",
        "    scheduled_datetime_local = scheduled_datetime.astimezone(recipient_timezone)\n",
        "\n",
        "    # Définir la date d'envoi programmée dans l'e-mail\n",
        "    msg['Date'] = formatdate(float(scheduled_datetime_local.strftime('%s')))\n",
        "\n",
        "    # Corps de l'e-mail\n",
        "    body_text = f\"\"\"\n",
        "    Cher(e) ami(e),\n",
        "\n",
        "    Nous espérons que vous allez bien. Chez L'Oréal, nous accordons une grande importance à votre avis et aimerions vous inviter à participer à notre enquête de satisfaction.\n",
        "\n",
        "    Nous vous invitons cordialement à participer à notre enquête de satisfaction client. Cela ne prendra que quelques minutes, et vous y gagnerez des réductions valables dès votre prochaine commande.\n",
        "    Avez vous aimé votre produit référence : paf99e70-af1b-4ba5-b42a-95067d82770e\n",
        "    Cliquez sur le lien ci-dessous pour accéder à l'enquête :\n",
        "    {survey_link}\n",
        "\n",
        "    Merci de prendre le temps de partager vos commentaires. Votre contribution est précieuse pour nous.\n",
        "\n",
        "    Cordialement,\n",
        "    Eugène Schueller\n",
        "    Responsable service consomateur\n",
        "    L'Oréol\n",
        "    \"\"\"\n",
        "\n",
        "    msg.attach(MIMEText(body_text, 'plain'))\n",
        "\n",
        "    # Connexion au serveur SMTP\n",
        "    with smtplib.SMTP(smtp_server, smtp_port) as server:\n",
        "        # Démarrer le chiffrement TLS (si nécessaire)\n",
        "        server.starttls()\n",
        "\n",
        "        # Authentification auprès du serveur SMTP\n",
        "        server.login(sender_email, sender_password)\n",
        "\n",
        "        # Envoi de l'e-mail\n",
        "        server.sendmail(sender_email, to_email, msg.as_string())\n",
        "\n",
        "# Exemple d'utilisation\n",
        "send_email('client@gmail.com', 'Invitation à participer à notre enquête de satisfaction', 'body', 'scheduled_time', 'entreprise@gmail.com', 'mot de passe', 'smtp.gmail.com', 25, 'https://docs.google.com/forms/d/e/1FAIpQLSeu0BKknzed47oK1i1a5ZnaiYeXNFGAjLAk01LRkH2xXApM1g/viewform')\n"
      ],
      "metadata": {
        "id": "597itr00xKyj"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "_8-Fr-uHx_zp"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "# ***IMPORT DE LA BASE DE DONNEES RECOLTEES GRACE A NOTRE ENQUETE DE SATISFACTION ENVOYEE PAR MAIL***"
      ],
      "metadata": {
        "id": "HiCnQv-vEzVw"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "spreadsheet_key = \"1Tlxu5P1gBhg_0Gyg06547y-fCxBnhz5qJL9X3OKsnRQ\" #ID de l'enquête\n",
        "df = pd.read_csv(f\"https://docs.google.com/spreadsheets/d/{spreadsheet_key}/export?format=csv\") #Import de l'enquête en csv sur python"
      ],
      "metadata": {
        "id": "wcsCkF1vSm2A"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#df = pd.read_csv(f\"https://docs.google.com/spreadsheets/d/{spreadsheet_key}/export?format=csv\") #Import de l'enquête en csv sur python"
      ],
      "metadata": {
        "id": "2qwhyQ2ORMGl"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "**CHANGEMENT DES NOMS DES COLONNES**"
      ],
      "metadata": {
        "id": "tsbEK91dE944"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "df.rename(columns={'Remarque globale sur le service proposé.': 'Avis'}, inplace=True)\n",
        "df.rename(columns={'Horodateur': 'Time'}, inplace=True)\n",
        "df.rename(columns={'Quelle sont les références des produits que vous avez commandés ? (3 références maximum séparées par des virgules.)': 'productid'}, inplace=True)\n",
        "df.rename(columns={'Quelle opinion avez vous du premier produit que vous avez commandé ?': 'opinion'}, inplace=True)\n",
        "df"
      ],
      "metadata": {
        "id": "MM-SwGwCkon9",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 738
        },
        "outputId": "9b677dbe-971e-4d06-8387-781ea8a93f88"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                   Time  \\\n",
              "0   18/01/2024 11:37:14   \n",
              "1   18/01/2024 14:32:33   \n",
              "2   18/01/2024 16:11:01   \n",
              "3   18/01/2024 18:04:11   \n",
              "4   18/01/2024 18:25:11   \n",
              "5   18/01/2024 18:32:00   \n",
              "6   19/01/2024 08:56:52   \n",
              "7   19/01/2024 09:31:42   \n",
              "8   19/01/2024 09:36:16   \n",
              "9   19/01/2024 09:44:50   \n",
              "10  19/01/2024 09:52:59   \n",
              "11  19/01/2024 10:30:50   \n",
              "\n",
              "   Rentrez la référence du produit que vous souhaitez évalué.  \\\n",
              "0                p5e85975-ef21-4976-a6b0-73e6afda3e5c           \n",
              "1        p5e85975-ef21-4976-a6b0-73e6afda3e5c                   \n",
              "2                p5e85975-ef21-4976-a6b0-73e6afda3e5c           \n",
              "3                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "4                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "5                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "6                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "7                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "8                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "9                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "10               paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "11               paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "\n",
              "   Quelle opinion avez vous de ce produit ?   \\\n",
              "0                                 Très bonne   \n",
              "1                             Assez mauavsie   \n",
              "2                                      Bonne   \n",
              "3                                      Bonne   \n",
              "4                                      Bonne   \n",
              "5                                 Très bonne   \n",
              "6                                 Très bonne   \n",
              "7                                 Très bonne   \n",
              "8                                 Très bonne   \n",
              "9                                 Très bonne   \n",
              "10                                Très bonne   \n",
              "11                                Très bonne   \n",
              "\n",
              "                                                 Avis           Adresse e-mail  \n",
              "0   Super produit pour ma peau sèche je recommande...  stanlesieur77@gmail.com  \n",
              "1   Super Super Super Super Super Super Super Supe...  stanlesieur77@gmail.com  \n",
              "2   Vraiment génial, produit assez efficace je rec...  stanlesieur77@gmail.com  \n",
              "3                                    Très bon produit  stanlesieur77@gmail.com  \n",
              "4                  Super produit vainqueur hackathon   stanlesieur77@gmail.com  \n",
              "5   Géniale j'espère que nous sommes les vainqueur...  stanlesieur77@gmail.com  \n",
              "6                     super produit vive le hackathon  stanlesieur77@gmail.com  \n",
              "7                     super produit vive le hackathon  stanlesieur77@gmail.com  \n",
              "8                             Super produit Hackathon  stanlesieur77@gmail.com  \n",
              "9                                   Vive le hackathon  stanlesieur77@gmail.com  \n",
              "10                                  Vive le hackathon  stanlesieur77@gmail.com  \n",
              "11                                  Vive le hackathon  stanlesieur77@gmail.com  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-7b19fdfd-d6e3-440e-b084-70d725ad9a30\" class=\"colab-df-container\">\n",
              "    <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Time</th>\n",
              "      <th>Rentrez la référence du produit que vous souhaitez évalué.</th>\n",
              "      <th>Quelle opinion avez vous de ce produit ?</th>\n",
              "      <th>Avis</th>\n",
              "      <th>Adresse e-mail</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>18/01/2024 11:37:14</td>\n",
              "      <td>p5e85975-ef21-4976-a6b0-73e6afda3e5c</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Super produit pour ma peau sèche je recommande...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>18/01/2024 14:32:33</td>\n",
              "      <td>p5e85975-ef21-4976-a6b0-73e6afda3e5c</td>\n",
              "      <td>Assez mauavsie</td>\n",
              "      <td>Super Super Super Super Super Super Super Supe...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>18/01/2024 16:11:01</td>\n",
              "      <td>p5e85975-ef21-4976-a6b0-73e6afda3e5c</td>\n",
              "      <td>Bonne</td>\n",
              "      <td>Vraiment génial, produit assez efficace je rec...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>18/01/2024 18:04:11</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Bonne</td>\n",
              "      <td>Très bon produit</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>18/01/2024 18:25:11</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Bonne</td>\n",
              "      <td>Super produit vainqueur hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>18/01/2024 18:32:00</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Géniale j'espère que nous sommes les vainqueur...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>19/01/2024 08:56:52</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>super produit vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>19/01/2024 09:31:42</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>super produit vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>19/01/2024 09:36:16</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Super produit Hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>19/01/2024 09:44:50</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>19/01/2024 09:52:59</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>19/01/2024 10:30:50</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "    <div class=\"colab-df-buttons\">\n",
              "\n",
              "  <div class=\"colab-df-container\">\n",
              "    <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-7b19fdfd-d6e3-440e-b084-70d725ad9a30')\"\n",
              "            title=\"Convert this dataframe to an interactive table.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\">\n",
              "    <path d=\"M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "\n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    .colab-df-buttons div {\n",
              "      margin-bottom: 4px;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "    <script>\n",
              "      const buttonEl =\n",
              "        document.querySelector('#df-7b19fdfd-d6e3-440e-b084-70d725ad9a30 button.colab-df-convert');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      async function convertToInteractive(key) {\n",
              "        const element = document.querySelector('#df-7b19fdfd-d6e3-440e-b084-70d725ad9a30');\n",
              "        const dataTable =\n",
              "          await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                    [key], {});\n",
              "        if (!dataTable) return;\n",
              "\n",
              "        const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "          '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "          + ' to learn more about interactive tables.';\n",
              "        element.innerHTML = '';\n",
              "        dataTable['output_type'] = 'display_data';\n",
              "        await google.colab.output.renderOutput(dataTable, element);\n",
              "        const docLink = document.createElement('div');\n",
              "        docLink.innerHTML = docLinkHtml;\n",
              "        element.appendChild(docLink);\n",
              "      }\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "\n",
              "<div id=\"df-7fc889e3-095b-404d-8564-812d6bb178c5\">\n",
              "  <button class=\"colab-df-quickchart\" onclick=\"quickchart('df-7fc889e3-095b-404d-8564-812d6bb178c5')\"\n",
              "            title=\"Suggest charts\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "     width=\"24px\">\n",
              "    <g>\n",
              "        <path d=\"M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z\"/>\n",
              "    </g>\n",
              "</svg>\n",
              "  </button>\n",
              "\n",
              "<style>\n",
              "  .colab-df-quickchart {\n",
              "      --bg-color: #E8F0FE;\n",
              "      --fill-color: #1967D2;\n",
              "      --hover-bg-color: #E2EBFA;\n",
              "      --hover-fill-color: #174EA6;\n",
              "      --disabled-fill-color: #AAA;\n",
              "      --disabled-bg-color: #DDD;\n",
              "  }\n",
              "\n",
              "  [theme=dark] .colab-df-quickchart {\n",
              "      --bg-color: #3B4455;\n",
              "      --fill-color: #D2E3FC;\n",
              "      --hover-bg-color: #434B5C;\n",
              "      --hover-fill-color: #FFFFFF;\n",
              "      --disabled-bg-color: #3B4455;\n",
              "      --disabled-fill-color: #666;\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart {\n",
              "    background-color: var(--bg-color);\n",
              "    border: none;\n",
              "    border-radius: 50%;\n",
              "    cursor: pointer;\n",
              "    display: none;\n",
              "    fill: var(--fill-color);\n",
              "    height: 32px;\n",
              "    padding: 0;\n",
              "    width: 32px;\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart:hover {\n",
              "    background-color: var(--hover-bg-color);\n",
              "    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "    fill: var(--button-hover-fill-color);\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart-complete:disabled,\n",
              "  .colab-df-quickchart-complete:disabled:hover {\n",
              "    background-color: var(--disabled-bg-color);\n",
              "    fill: var(--disabled-fill-color);\n",
              "    box-shadow: none;\n",
              "  }\n",
              "\n",
              "  .colab-df-spinner {\n",
              "    border: 2px solid var(--fill-color);\n",
              "    border-color: transparent;\n",
              "    border-bottom-color: var(--fill-color);\n",
              "    animation:\n",
              "      spin 1s steps(1) infinite;\n",
              "  }\n",
              "\n",
              "  @keyframes spin {\n",
              "    0% {\n",
              "      border-color: transparent;\n",
              "      border-bottom-color: var(--fill-color);\n",
              "      border-left-color: var(--fill-color);\n",
              "    }\n",
              "    20% {\n",
              "      border-color: transparent;\n",
              "      border-left-color: var(--fill-color);\n",
              "      border-top-color: var(--fill-color);\n",
              "    }\n",
              "    30% {\n",
              "      border-color: transparent;\n",
              "      border-left-color: var(--fill-color);\n",
              "      border-top-color: var(--fill-color);\n",
              "      border-right-color: var(--fill-color);\n",
              "    }\n",
              "    40% {\n",
              "      border-color: transparent;\n",
              "      border-right-color: var(--fill-color);\n",
              "      border-top-color: var(--fill-color);\n",
              "    }\n",
              "    60% {\n",
              "      border-color: transparent;\n",
              "      border-right-color: var(--fill-color);\n",
              "    }\n",
              "    80% {\n",
              "      border-color: transparent;\n",
              "      border-right-color: var(--fill-color);\n",
              "      border-bottom-color: var(--fill-color);\n",
              "    }\n",
              "    90% {\n",
              "      border-color: transparent;\n",
              "      border-bottom-color: var(--fill-color);\n",
              "    }\n",
              "  }\n",
              "</style>\n",
              "\n",
              "  <script>\n",
              "    async function quickchart(key) {\n",
              "      const quickchartButtonEl =\n",
              "        document.querySelector('#' + key + ' button');\n",
              "      quickchartButtonEl.disabled = true;  // To prevent multiple clicks.\n",
              "      quickchartButtonEl.classList.add('colab-df-spinner');\n",
              "      try {\n",
              "        const charts = await google.colab.kernel.invokeFunction(\n",
              "            'suggestCharts', [key], {});\n",
              "      } catch (error) {\n",
              "        console.error('Error during call to suggestCharts:', error);\n",
              "      }\n",
              "      quickchartButtonEl.classList.remove('colab-df-spinner');\n",
              "      quickchartButtonEl.classList.add('colab-df-quickchart-complete');\n",
              "    }\n",
              "    (() => {\n",
              "      let quickchartButtonEl =\n",
              "        document.querySelector('#df-7fc889e3-095b-404d-8564-812d6bb178c5 button');\n",
              "      quickchartButtonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "    })();\n",
              "  </script>\n",
              "</div>\n",
              "    </div>\n",
              "  </div>\n"
            ]
          },
          "metadata": {},
          "execution_count": 6
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "**PROCESSUS DE NETTOYAGE DES AVIS RECOLTES**"
      ],
      "metadata": {
        "id": "3zl2_q-QFFTo"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import nltk\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.tokenize import word_tokenize\n",
        "from nltk.probability import FreqDist\n",
        "\n",
        "nltk.download('punkt')\n",
        "nltk.download('stopwords')"
      ],
      "metadata": {
        "id": "kSOqO6ii2kw0"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import string\n",
        "import nltk\n",
        "nltk.download('popular')\n",
        "\n",
        "from nltk import word_tokenize\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.corpus import stopwords\n",
        "\n",
        "#Téléchargez les stopwords pour le français\n",
        "nltk.download('stopwords')\n",
        "stopwords_fr = set(stopwords.words(\"french\"))\n",
        "\n",
        "def fclean(texte):\n",
        "    words = word_tokenize(texte, language='french')  # Spécifiez la langue comme français\n",
        "\n",
        "    words_tout = []\n",
        "    for w in words:\n",
        "        if w.isalpha():\n",
        "            words_tout.append(w.lower())\n",
        "\n",
        "    words_clean = []\n",
        "    for w in words_tout:\n",
        "        if w not in stopwords_fr:\n",
        "            words_clean.append(w)\n",
        "\n",
        "    wclean = \" \".join(words_clean)\n",
        "    return wclean"
      ],
      "metadata": {
        "id": "Znvz-N0CqER5"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "texte = \"Bonjour, comment ça va aujourd'hui ?\"\n",
        "print(fclean(texte))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BSB-ZQ05qKHZ",
        "outputId": "a3131e47-c57e-48bc-bbad-737dcd8fb0fb"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "bonjour comment ça va\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "**CREATION D'UNE COLONNE DES AVIS NETTOYES**"
      ],
      "metadata": {
        "id": "OFXXbhnkFYh6"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "df['avisclean'] = df['Avis'].apply(lambda x : fclean(str(x)))"
      ],
      "metadata": {
        "id": "J96Nm0-rylLF"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "df"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 981
        },
        "id": "wxDvmG4omov0",
        "outputId": "5ec467a0-c4a9-43a6-b693-56c67bd7eac1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                   Time  \\\n",
              "0   18/01/2024 11:37:14   \n",
              "1   18/01/2024 14:32:33   \n",
              "2   18/01/2024 16:11:01   \n",
              "3   18/01/2024 18:04:11   \n",
              "4   18/01/2024 18:25:11   \n",
              "5   18/01/2024 18:32:00   \n",
              "6   19/01/2024 08:56:52   \n",
              "7   19/01/2024 09:31:42   \n",
              "8   19/01/2024 09:36:16   \n",
              "9   19/01/2024 09:44:50   \n",
              "10  19/01/2024 09:52:59   \n",
              "11  19/01/2024 10:30:50   \n",
              "\n",
              "   Rentrez la référence du produit que vous souhaitez évalué.  \\\n",
              "0                p5e85975-ef21-4976-a6b0-73e6afda3e5c           \n",
              "1        p5e85975-ef21-4976-a6b0-73e6afda3e5c                   \n",
              "2                p5e85975-ef21-4976-a6b0-73e6afda3e5c           \n",
              "3                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "4                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "5                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "6                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "7                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "8                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "9                paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "10               paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "11               paf99e70-af1b-4ba5-b42a-95067d82770e           \n",
              "\n",
              "   Quelle opinion avez vous de ce produit ?   \\\n",
              "0                                 Très bonne   \n",
              "1                             Assez mauavsie   \n",
              "2                                      Bonne   \n",
              "3                                      Bonne   \n",
              "4                                      Bonne   \n",
              "5                                 Très bonne   \n",
              "6                                 Très bonne   \n",
              "7                                 Très bonne   \n",
              "8                                 Très bonne   \n",
              "9                                 Très bonne   \n",
              "10                                Très bonne   \n",
              "11                                Très bonne   \n",
              "\n",
              "                                                 Avis  \\\n",
              "0   Super produit pour ma peau sèche je recommande...   \n",
              "1   Super Super Super Super Super Super Super Supe...   \n",
              "2   Vraiment génial, produit assez efficace je rec...   \n",
              "3                                    Très bon produit   \n",
              "4                  Super produit vainqueur hackathon    \n",
              "5   Géniale j'espère que nous sommes les vainqueur...   \n",
              "6                     super produit vive le hackathon   \n",
              "7                     super produit vive le hackathon   \n",
              "8                             Super produit Hackathon   \n",
              "9                                   Vive le hackathon   \n",
              "10                                  Vive le hackathon   \n",
              "11                                  Vive le hackathon   \n",
              "\n",
              "             Adresse e-mail                                          avisclean  \n",
              "0   stanlesieur77@gmail.com       super produit peau sèche recommande vivement  \n",
              "1   stanlesieur77@gmail.com  super super super super super super super supe...  \n",
              "2   stanlesieur77@gmail.com  vraiment génial produit assez efficace recommande  \n",
              "3   stanlesieur77@gmail.com                                   très bon produit  \n",
              "4   stanlesieur77@gmail.com                  super produit vainqueur hackathon  \n",
              "5   stanlesieur77@gmail.com                       géniale vainqueurs hackathon  \n",
              "6   stanlesieur77@gmail.com                       super produit vive hackathon  \n",
              "7   stanlesieur77@gmail.com                       super produit vive hackathon  \n",
              "8   stanlesieur77@gmail.com                            super produit hackathon  \n",
              "9   stanlesieur77@gmail.com                                     vive hackathon  \n",
              "10  stanlesieur77@gmail.com                                     vive hackathon  \n",
              "11  stanlesieur77@gmail.com                                     vive hackathon  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-ff7cf171-bde8-45d1-b3d7-33ac306ed8e8\" class=\"colab-df-container\">\n",
              "    <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Time</th>\n",
              "      <th>Rentrez la référence du produit que vous souhaitez évalué.</th>\n",
              "      <th>Quelle opinion avez vous de ce produit ?</th>\n",
              "      <th>Avis</th>\n",
              "      <th>Adresse e-mail</th>\n",
              "      <th>avisclean</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>18/01/2024 11:37:14</td>\n",
              "      <td>p5e85975-ef21-4976-a6b0-73e6afda3e5c</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Super produit pour ma peau sèche je recommande...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>super produit peau sèche recommande vivement</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>18/01/2024 14:32:33</td>\n",
              "      <td>p5e85975-ef21-4976-a6b0-73e6afda3e5c</td>\n",
              "      <td>Assez mauavsie</td>\n",
              "      <td>Super Super Super Super Super Super Super Supe...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>super super super super super super super supe...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>18/01/2024 16:11:01</td>\n",
              "      <td>p5e85975-ef21-4976-a6b0-73e6afda3e5c</td>\n",
              "      <td>Bonne</td>\n",
              "      <td>Vraiment génial, produit assez efficace je rec...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>vraiment génial produit assez efficace recommande</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>18/01/2024 18:04:11</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Bonne</td>\n",
              "      <td>Très bon produit</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>très bon produit</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>18/01/2024 18:25:11</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Bonne</td>\n",
              "      <td>Super produit vainqueur hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>super produit vainqueur hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>18/01/2024 18:32:00</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Géniale j'espère que nous sommes les vainqueur...</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>géniale vainqueurs hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>19/01/2024 08:56:52</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>super produit vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>super produit vive hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>19/01/2024 09:31:42</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>super produit vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>super produit vive hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>19/01/2024 09:36:16</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Super produit Hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>super produit hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>19/01/2024 09:44:50</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>vive hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>19/01/2024 09:52:59</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>vive hackathon</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>19/01/2024 10:30:50</td>\n",
              "      <td>paf99e70-af1b-4ba5-b42a-95067d82770e</td>\n",
              "      <td>Très bonne</td>\n",
              "      <td>Vive le hackathon</td>\n",
              "      <td>stanlesieur77@gmail.com</td>\n",
              "      <td>vive hackathon</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "    <div class=\"colab-df-buttons\">\n",
              "\n",
              "  <div class=\"colab-df-container\">\n",
              "    <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-ff7cf171-bde8-45d1-b3d7-33ac306ed8e8')\"\n",
              "            title=\"Convert this dataframe to an interactive table.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\">\n",
              "    <path d=\"M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "\n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    .colab-df-buttons div {\n",
              "      margin-bottom: 4px;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "    <script>\n",
              "      const buttonEl =\n",
              "        document.querySelector('#df-ff7cf171-bde8-45d1-b3d7-33ac306ed8e8 button.colab-df-convert');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      async function convertToInteractive(key) {\n",
              "        const element = document.querySelector('#df-ff7cf171-bde8-45d1-b3d7-33ac306ed8e8');\n",
              "        const dataTable =\n",
              "          await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                    [key], {});\n",
              "        if (!dataTable) return;\n",
              "\n",
              "        const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "          '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "          + ' to learn more about interactive tables.';\n",
              "        element.innerHTML = '';\n",
              "        dataTable['output_type'] = 'display_data';\n",
              "        await google.colab.output.renderOutput(dataTable, element);\n",
              "        const docLink = document.createElement('div');\n",
              "        docLink.innerHTML = docLinkHtml;\n",
              "        element.appendChild(docLink);\n",
              "      }\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "\n",
              "<div id=\"df-628b677d-49a8-425d-a2b0-68d3e66e9bfb\">\n",
              "  <button class=\"colab-df-quickchart\" onclick=\"quickchart('df-628b677d-49a8-425d-a2b0-68d3e66e9bfb')\"\n",
              "            title=\"Suggest charts\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "     width=\"24px\">\n",
              "    <g>\n",
              "        <path d=\"M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z\"/>\n",
              "    </g>\n",
              "</svg>\n",
              "  </button>\n",
              "\n",
              "<style>\n",
              "  .colab-df-quickchart {\n",
              "      --bg-color: #E8F0FE;\n",
              "      --fill-color: #1967D2;\n",
              "      --hover-bg-color: #E2EBFA;\n",
              "      --hover-fill-color: #174EA6;\n",
              "      --disabled-fill-color: #AAA;\n",
              "      --disabled-bg-color: #DDD;\n",
              "  }\n",
              "\n",
              "  [theme=dark] .colab-df-quickchart {\n",
              "      --bg-color: #3B4455;\n",
              "      --fill-color: #D2E3FC;\n",
              "      --hover-bg-color: #434B5C;\n",
              "      --hover-fill-color: #FFFFFF;\n",
              "      --disabled-bg-color: #3B4455;\n",
              "      --disabled-fill-color: #666;\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart {\n",
              "    background-color: var(--bg-color);\n",
              "    border: none;\n",
              "    border-radius: 50%;\n",
              "    cursor: pointer;\n",
              "    display: none;\n",
              "    fill: var(--fill-color);\n",
              "    height: 32px;\n",
              "    padding: 0;\n",
              "    width: 32px;\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart:hover {\n",
              "    background-color: var(--hover-bg-color);\n",
              "    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "    fill: var(--button-hover-fill-color);\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart-complete:disabled,\n",
              "  .colab-df-quickchart-complete:disabled:hover {\n",
              "    background-color: var(--disabled-bg-color);\n",
              "    fill: var(--disabled-fill-color);\n",
              "    box-shadow: none;\n",
              "  }\n",
              "\n",
              "  .colab-df-spinner {\n",
              "    border: 2px solid var(--fill-color);\n",
              "    border-color: transparent;\n",
              "    border-bottom-color: var(--fill-color);\n",
              "    animation:\n",
              "      spin 1s steps(1) infinite;\n",
              "  }\n",
              "\n",
              "  @keyframes spin {\n",
              "    0% {\n",
              "      border-color: transparent;\n",
              "      border-bottom-color: var(--fill-color);\n",
              "      border-left-color: var(--fill-color);\n",
              "    }\n",
              "    20% {\n",
              "      border-color: transparent;\n",
              "      border-left-color: var(--fill-color);\n",
              "      border-top-color: var(--fill-color);\n",
              "    }\n",
              "    30% {\n",
              "      border-color: transparent;\n",
              "      border-left-color: var(--fill-color);\n",
              "      border-top-color: var(--fill-color);\n",
              "      border-right-color: var(--fill-color);\n",
              "    }\n",
              "    40% {\n",
              "      border-color: transparent;\n",
              "      border-right-color: var(--fill-color);\n",
              "      border-top-color: var(--fill-color);\n",
              "    }\n",
              "    60% {\n",
              "      border-color: transparent;\n",
              "      border-right-color: var(--fill-color);\n",
              "    }\n",
              "    80% {\n",
              "      border-color: transparent;\n",
              "      border-right-color: var(--fill-color);\n",
              "      border-bottom-color: var(--fill-color);\n",
              "    }\n",
              "    90% {\n",
              "      border-color: transparent;\n",
              "      border-bottom-color: var(--fill-color);\n",
              "    }\n",
              "  }\n",
              "</style>\n",
              "\n",
              "  <script>\n",
              "    async function quickchart(key) {\n",
              "      const quickchartButtonEl =\n",
              "        document.querySelector('#' + key + ' button');\n",
              "      quickchartButtonEl.disabled = true;  // To prevent multiple clicks.\n",
              "      quickchartButtonEl.classList.add('colab-df-spinner');\n",
              "      try {\n",
              "        const charts = await google.colab.kernel.invokeFunction(\n",
              "            'suggestCharts', [key], {});\n",
              "      } catch (error) {\n",
              "        console.error('Error during call to suggestCharts:', error);\n",
              "      }\n",
              "      quickchartButtonEl.classList.remove('colab-df-spinner');\n",
              "      quickchartButtonEl.classList.add('colab-df-quickchart-complete');\n",
              "    }\n",
              "    (() => {\n",
              "      let quickchartButtonEl =\n",
              "        document.querySelector('#df-628b677d-49a8-425d-a2b0-68d3e66e9bfb button');\n",
              "      quickchartButtonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "    })();\n",
              "  </script>\n",
              "</div>\n",
              "    </div>\n",
              "  </div>\n"
            ]
          },
          "metadata": {},
          "execution_count": 11
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# ***PARTI WORDCLOUD POUR VOIR LES TERMES/SENTIMENTS QUI SORTENT LE PLUS***"
      ],
      "metadata": {
        "id": "hNJNZLFZEQlE"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import matplotlib.pyplot as plt\n",
        "from wordcloud import WordCloud"
      ],
      "metadata": {
        "id": "KGpbnD7pvGho"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "texte_concatene = ' '.join(df['avisclean'])"
      ],
      "metadata": {
        "id": "Y_gKSmd1wYyF"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Generate the word cloud\n",
        "wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texte_concatene)\n",
        "\n",
        "# Display the word cloud using matplotlib\n",
        "plt.figure(figsize=(10, 5))\n",
        "plt.imshow(wordcloud, interpolation='bilinear')\n",
        "plt.axis('off')\n",
        "plt.show()"
      ],
      "metadata": {
        "id": "UxWCH3OL6ERj",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 422
        },
        "outputId": "1f545ff4-0606-48da-9cfe-d82622d9ad09"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1000x500 with 1 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# ***PARTI MACHINE LEARNING POUR PROPOSER DES PRODUITS SUSCEPTIBLES DE PLAIRE AU CLIENT EN FONCTION DE CES PRODUITS COMMANDES***"
      ],
      "metadata": {
        "id": "4fv80_tpFxcR"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt\n",
        "import numpy as np"
      ],
      "metadata": {
        "id": "vBfSgkCCY3JX"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8O6QF5AWY5lF",
        "outputId": "0e669e88-8c73-4f11-ac89-91d4ff76481d"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount(\"/content/drive\", force_remount=True).\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "df = pd.read_csv(\"/content/drive/MyDrive/JALMS-HACKATHON/machine learning/merge_laureol_b_to_c _df.csv\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "po-D2rfVZADV",
        "outputId": "80f46260-61f0-4625-905e-53cd134a8717"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "<ipython-input-17-0aad3a4ec00a>:2: DtypeWarning: Columns (12) have mixed types. Specify dtype option on import or set low_memory=False.\n",
            "  df = pd.read_csv(\"/content/drive/MyDrive/JALMS-HACKATHON/machine learning/merge_laureol_b_to_c _df.csv\")\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "df2 = pd.read_csv(\"/content/drive/MyDrive/JALMS-HACKATHON/machine learning/merge_table_laureol_b_to_c_df2.csv\")"
      ],
      "metadata": {
        "id": "Yq9dh4xRZAAC",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "139e8f80-9a1b-47eb-a379-70ccca4791a3"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "<ipython-input-18-32b48152ee5c>:1: DtypeWarning: Columns (5) have mixed types. Specify dtype option on import or set low_memory=False.\n",
            "  df2 = pd.read_csv(\"/content/drive/MyDrive/JALMS-HACKATHON/machine learning/merge_table_laureol_b_to_c_df2.csv\")\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def produits_voisins(Idproduit, df, df2):\n",
        "\n",
        "    df3 = df2.iloc[0:2000000]\n",
        "    X= df3[['gender', 'OptinValue', 'productBasePrice', 'productQuantity',\n",
        "       'productTotalPrice', 'brand', 'productCategory',\n",
        "       'totalAmount', 'totalQuantity']]\n",
        "    y= df3['productId']\n",
        "    from sklearn.neighbors import NearestNeighbors\n",
        "\n",
        "    modelNN = NearestNeighbors(n_neighbors = 4)\n",
        "    modelNN.fit(X)\n",
        "    neighbors = modelNN.kneighbors(df3.loc[df3['productId'] == Idproduit, X.columns])\n",
        "\n",
        "    voisins = neighbors[1][0]\n",
        "    produits = df3['productId'].iloc[voisins]\n",
        "\n",
        "    noms_voisins = []\n",
        "    for nom in df3['productId'].iloc[voisins][1:]:\n",
        "        print(nom)\n",
        "        noms_voisins.append(df[df['productId'] == nom]['productName'].unique()[0])\n",
        "    return noms_voisins"
      ],
      "metadata": {
        "id": "rJgCkPk_28rj"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "liste = produits_voisins('paf99e70-af1b-4ba5-b42a-95067d82770e', df, df2)"
      ],
      "metadata": {
        "id": "tk2Q5NiKTrAt",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "ba41230d-10ca-4340-e413-f6bd06e48ef9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "paf99e70-af1b-4ba5-b42a-95067d82770e\n",
            "pcfa3b3a-1fcd-4756-af9a-4829be4505ec\n",
            "pcfa3b3a-1fcd-4756-af9a-4829be4505ec\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "liste"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "0_d-sZ4lcPmK",
        "outputId": "d12447f9-7d61-4644-d56c-4232c0fe454b"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['Trade Sister', 'Several Board', 'Several Board']"
            ]
          },
          "metadata": {},
          "execution_count": 21
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "rp1 = liste[0]\n",
        "rp1"
      ],
      "metadata": {
        "id": "2eXRb2-H28op",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 35
        },
        "outputId": "40218787-7158-4965-fb5a-c9d1dceef368"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'Trade Sister'"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            }
          },
          "metadata": {},
          "execution_count": 22
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "rp2= liste[2]\n",
        "rp2"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 35
        },
        "id": "iG5p50LYbE-F",
        "outputId": "32f9fca8-8ab9-4192-9c48-f2ab852d5a8a"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'Several Board'"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            }
          },
          "metadata": {},
          "execution_count": 23
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "H-yGp4Y7cphv"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "# ***ENVOI DU SECOND MAIL AU CLIENT AVEC LE CODE DE REDUCTION ET L'ASSISTANT***"
      ],
      "metadata": {
        "id": "Y6MeCHD4EDGe"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "scheduled_time = '2024-01-17 10:00:00'\n",
        "scheduled_datetime = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')\n",
        "\n",
        "def send_email(to_email, subject, body, scheduled_time, sender_email, sender_password, smtp_server, smtp_port, survey_link, rp1, rp2,lienproduit):\n",
        "    msg = MIMEMultipart()\n",
        "    msg['From'] = sender_email\n",
        "    msg['To'] = to_email\n",
        "    msg['Subject'] = subject\n",
        "\n",
        "    # Convertir le temps programmé en format de date et heure\n",
        "    #scheduled_datetime = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')\n",
        "\n",
        "    # Récupérer le fuseau horaire local du destinataire\n",
        "    recipient_timezone = pytz.timezone('Europe/Paris')  # Remplacez 'Europe/Paris' par le fuseau horaire du destinataire\n",
        "\n",
        "    # Convertir le temps programmé au fuseau horaire local du destinataire\n",
        "    scheduled_datetime_local = scheduled_datetime.astimezone(recipient_timezone)\n",
        "\n",
        "    # Définir la date d'envoi programmée dans l'e-mail\n",
        "    msg['Date'] = formatdate(float(scheduled_datetime_local.strftime('%s')))\n",
        "\n",
        "    # Corps de l'e-mail\n",
        "    body_text = f\"\"\"\n",
        "    Cher(e) ami(e),\n",
        "\n",
        "    Nous espérons que vous allez bien. Nous vous remercions d'avoir pris le temps de répondre à notre enquête de satisfaction.\n",
        "\n",
        "    Voici la remise promise pour nous avoir aidé à amélioré notre service : 'HACKATHON10'\n",
        "    Profitez de 10% de réductions sur votre prochaine commande valable 14 jours après réception.\n",
        "\n",
        "    Nous vous conseillons ces références de notre catalogue en fonction de vos derniers achats :\n",
        "    {rp1, rp2} {lienproduit}\n",
        "\n",
        "    Et si vous avez des questions sur nos produits hésitez pas à utiliser notre assistant virtuel :\n",
        "    {survey_link}\n",
        "\n",
        "    Merci de prendre le temps de partager vos commentaires. Votre contribution est précieuse pour nous.\n",
        "\n",
        "    Cordialement,\n",
        "    Eugène Schueller\n",
        "    Responsable service consomateur\n",
        "    L'Oréol\n",
        "    \"\"\"\n",
        "\n",
        "    msg.attach(MIMEText(body_text, 'plain'))\n",
        "\n",
        "    # Connexion au serveur SMTP\n",
        "    with smtplib.SMTP(smtp_server, smtp_port) as server:\n",
        "        # Démarrer le chiffrement TLS (si nécessaire)\n",
        "        server.starttls()\n",
        "\n",
        "        # Authentification auprès du serveur SMTP\n",
        "        server.login(sender_email, sender_password)\n",
        "\n",
        "        # Envoi de l'e-mail\n",
        "        server.sendmail(sender_email, to_email, msg.as_string())\n",
        "\n",
        "# Exemple d'utilisation\n",
        "send_email(\"client@gmail.com\", \"L'Oréal : Merci de votre participation\", \"body\", \"scheduled_time\", \"entreprise@gmail.com\", \"mot de passe\", \"smtp.gmail.com\", 25, \"http://localhost:8501/\",rp1, rp2,\"https://www.loreal-paris.fr/soin/soin-par-categorie/soin-yeux/revitalift-yeux/OAP5037.html\")\n"
      ],
      "metadata": {
        "id": "lR0Cv5yw28mH"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}
