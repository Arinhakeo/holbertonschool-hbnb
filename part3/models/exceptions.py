class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)