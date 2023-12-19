import pandas as pd
from datetime import datetime
import re
import os
from datetime import datetime
import glob

# Pfad zur Datei, die transformiert werden soll
input_directory = './input'
output_directory = './output'

# Liste alle Excel-Dateien im Verzeichnis auf
excel_files = glob.glob(os.path.join(input_directory, '*.xlsx'))

def transform_to_zielformat_final_with_excel_dates(file_path):
    ursprungsformat_df = pd.read_excel(file_path)

    # Extrahieren der Spaltennamen, die "Woche" enthalten
    woche_columns = [col for col in ursprungsformat_df.columns if "Woche" in col]

    # Extraktion aller möglichen Tage aus den Wochenspalten
    all_dates = set()
    for col in woche_columns:
        for value in ursprungsformat_df[col].dropna().unique():
            dates = re.findall(r'\d{2}\.\d{2}\.\d{2}', value)
            all_dates.update(dates)
    all_dates = sorted(list(all_dates), key=lambda x: datetime.strptime(x, '%d.%m.%y'))

    # Umwandlung der Daten in das ISO-Format (z.B. "2023-07-14")
    all_dates_iso = [datetime.strptime(date, '%d.%m.%y').strftime('%Y-%m-%d') for date in all_dates]

    # Erstellen der neuen Spalten für jeden Tag
    new_columns = ['Name des Kindes', 'Klasse', 'geht alleine'] + all_dates_iso + ['Anmerkung']

    # Initialisierung des neuen DataFrames
    zielformat_df = pd.DataFrame(columns=new_columns)
    zielformat_df['Name des Kindes'] = ursprungsformat_df['Name des Kindes']
    zielformat_df['Klasse'] = ursprungsformat_df['Klasse']
    zielformat_df['Anmerkung'] = ''  # Initialisiere die Spalte 'Anmerkung' mit leeren Strings

    # Eintragen der Anwesenheitstage
    for index, row in ursprungsformat_df.iterrows():
        for col in woche_columns:
            if pd.notna(row[col]):
                dates = re.findall(r'\d{2}\.\d{2}\.\d{2}', row[col])
                for date in dates:
                    iso_date = datetime.strptime(date, '%d.%m.%y').strftime('%Y-%m-%d')
                    zielformat_df.at[index, iso_date] = 'x'

    # Extrahieren der Spaltennamen, die "Frühdienst" und "Spätdienst" enthalten
    fruehdienst_columns = [col for col in ursprungsformat_df.columns if "Frühdienst" in col]
    spaetdienst_columns = [col for col in ursprungsformat_df.columns if "Spätdienst" in col]

    # Abholsituation und Betreuungsdienste
    for index, row in ursprungsformat_df.iterrows():
        anmerkungen = []

        # Abholsituation
        if any("Kind geht allein" in str(row[col]) for col in ursprungsformat_df.columns[len(woche_columns) + 2:]):
            zielformat_df.at[index, 'geht alleine'] = 'A'

        # Frühdienst
        if any(row[col] == "JA (ab 7 Uhr)" for col in fruehdienst_columns):
            anmerkungen.append("Frühdienst")

        # Spätdienst
        if any(row[col] == "JA (bis 17 Uhr)" for col in spaetdienst_columns):
            anmerkungen.append("Spätdienst")

        # Überprüfung, ob das Kind an jedem Tag anwesend ist
        if all(zielformat_df.at[index, date] == 'x' for date in all_dates_iso):
            anmerkungen.insert(0, '#')

        # Hinzufügen der Anmerkungen zum DataFrame
        current_anmerkung = zielformat_df.at[index, 'Anmerkung']
        if current_anmerkung:
            zielformat_df.at[index, 'Anmerkung'] = ', '.join([current_anmerkung] + anmerkungen).strip(', ')
        else:
            zielformat_df.at[index, 'Anmerkung'] = ', '.join(anmerkungen).strip(', ')

    # Hinzufügen der letzten Zeile für die Gesamtanzahl der anwesenden Kinder pro Tag
    zielformat_df.loc['Gesamt'] = zielformat_df.iloc[:, 3:-1].apply(lambda x: x.count())

    # Zählen der Gesamtzahl der Kinder und Hinzufügen in die erste Spalte der letzten Zeile
    zielformat_df.at['Gesamt', 'Name des Kindes'] = zielformat_df['Name des Kindes'].count()

    # Zählen, wie viele Kinder an jedem Tag anwesend sind (Anzahl der "#")
    zielformat_df.at['Gesamt', 'Anmerkung'] = sum(zielformat_df['Anmerkung'].str.contains('#', na=False))

    # Sortieren der Daten nach Klasse und Name
    zielformat_df = zielformat_df.sort_values(by=['Klasse', 'Name des Kindes'])

    # Ersetzen von NaN durch leere Strings
    zielformat_df.fillna('', inplace=True)

    return zielformat_df

# Verarbeite jede Excel-Datei einzeln
for file in excel_files:
    transformed_df = transform_to_zielformat_final_with_excel_dates(file)

    # Erstelle einen Ausgabedateinamen basierend auf dem Originaldateinamen
    base_name = os.path.basename(file)
    output_file_path = os.path.join(output_directory, f'transformiertes_{base_name}')

    # Speichere die transformierte Datei
    transformed_df.to_excel(output_file_path, index=False)

print("Alle Dateien wurden verarbeitet.")