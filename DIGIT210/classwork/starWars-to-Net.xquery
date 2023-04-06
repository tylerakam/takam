let $starWarsColl := collection('ner-xml/?select=*.xml')
let $names := $starWarsColl//name !lower-case(.) ! normalize-space() => distinct-values()
let $speakers := $starWarsColl//speaker ! lower-case(.) ! normalize-space() => distinct-values()

for $s in $speakers
    let $movie := $starWarsColl[.//speaker ! lower-case(.) ! normalize-space() =$s] ! base-uri()
    let$movieTrimmed := $movie ! tokenize(.,'/')[last()]
    let $targetSp := $starWarsColl[.//speaker ! lower-case(.) ! normalize-space() =$s]//speaker[not(lower-case(.) ! normalize-space() = $s)]
    let $targetOtherNames := $starWarsColl[.//speaker ! lower-case(.) ! normalize-space() =$s]//name
    let $distinctSpeakers := $targetSp ! lower-case(.) ! normalize-space() => distinct-values()
    let $distinctOtherNames := $targetOtherNames ! lower-case(.) ! normalize-space() => distinct-values()
    
    
return $distinctOtherNames