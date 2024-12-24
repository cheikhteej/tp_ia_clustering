import pefile

"""
    Extrait les features spécifiées d'un fichier PE.
    Args:
        file_path (str): Chemin vers le fichier PE.
    Returns:
        dict: Dictionnaire contenant les features extraites.
"""

def extract_malware_features(file_path):
    try:
        pe = pefile.PE(file_path)

        features = {
            'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            'MajorLinkerVersion': pe.OPTIONAL_HEADER.MajorLinkerVersion,
            'MajorImageVersion': pe.OPTIONAL_HEADER.MajorImageVersion,
            'MajorOperatingSystemVersion': pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
            'DllCharacteristics': pe.OPTIONAL_HEADER.DllCharacteristics,
            'SizeOfStackReserve': pe.OPTIONAL_HEADER.SizeOfStackReserve,
            'NumberOfSections': len(pe.sections),
            'ResourceSize': sum(section.SizeOfRawData for section in pe.sections if section.Name == b'.rsrc')
        }

        return features
    except pefile.PEFormatError:
        print(f"Erreur lors de l'analyse de {file_path}: Fichier PE invalide")
        return None
