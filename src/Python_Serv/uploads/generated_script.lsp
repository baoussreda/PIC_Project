
    (defun c:CreateTVAntenna ()
        ; Define values for the TV antenna
        (setq basePoint '(10.0 10.0 0.0)) ; Replace with your desired base point (X, Y, Z)
        (setq mastHeight 10.0) ; Replace with the height of the mast
        (setq elementsHeight 5.0) ; Replace with the height of the antenna elements
        (setq elementLength 4.0) ; Replace with the length of each antenna element

        ; Calculate the endpoint of the mast
        (setq mastEndPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight)))

        ; Draw the mast as a line
        (command "LINE" basePoint mastEndPoint "")

        ; Draw the TV antenna elements as vertical lines
        (setq antennaStartPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight)))
        (setq antennaEndPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight elementsHeight)))

        (repeat 4
            (command "LINE" antennaStartPoint antennaEndPoint "")
            (setq antennaStartPoint antennaEndPoint)
            (setq antennaEndPoint (list (nth 0 basePoint) (nth 1 basePoint) (+ (nth 2 basePoint) mastHeight elementsHeight)))
        )

        ; Save the drawing (optional)
        (command "SAVEAS" "TVAntennaDrawing" "DWG")

        ; Close AutoCAD (optional)
        (command "QUIT" "Y")
    )

    ; Run the script immediately upon loading
    (c:CreateTVAntenna)
    