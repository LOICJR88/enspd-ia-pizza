
' ===========================================
' MACRO VBA - ENSPD IA PIZZA
' Envoie le texte (B4) à l'API Flask et affiche la réponse en B5/B6/B7
' Avant d'utiliser : Activer la référence "Microsoft Scripting Runtime"
' et "Microsoft XML, v6.0" dans Outils > Références (VBE)
' ===========================================

Sub EnvoyerCommande()
    Dim http As Object
    Dim url As String
    Dim body As String
    Dim sessionId As String
    Dim texte As String
    Dim response As String

    Set http = CreateObject("MSXML2.XMLHTTP")

    ' >>> REMPLACE PAR TON URL NGROK <
    url = "https://unfrozen-audience-remedial.ngrok-free.dev/order"

    sessionId = Range("B3").Value
    texte = Range("B4").Value

    body = "{""session_id"":""" & sessionId & """, ""text"":""" & texte & """}"

    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "application/json"
    http.send body

    response = http.responseText

    ' Affichage brut de la réponse JSON
    Range("B5").Value = response

    ' Extraction simple du "message" (entre guillemets après "message":)
    Dim posStart As Long, posEnd As Long
    posStart = InStr(response, """message"": """)
    If posStart > 0 Then
        posStart = posStart + Len("""message"": """)
        posEnd = InStr(posStart, response, """")
        Range("B5").Value = Mid(response, posStart, posEnd - posStart)
    End If

    Range("B6").Value = response

    MsgBox "Réponse reçue de l'IA Pizza !", vbInformation
End Sub
