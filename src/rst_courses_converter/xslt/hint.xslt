<stylesheet version="1.0"
            xmlns="http://www.w3.org/1999/XSL/Transform"
            xmlns:nn="http://nextnet.top/functions">

    <output
            method="text"
            version="string"
            encoding="utf-8"
            omit-xml-declaration="yes"
            standalone="yes"
            doctype-public="string"
            doctype-system="string"
            cdata-section-elements="namelist"
            indent="no"
            media-type="string"/>
    <template match="/paragraph">
        <apply-templates/>
    </template>

    <template match="/caution">
 > ### Astuce ###<text>&#xa;</text>
        <apply-templates/>
    </template>

    <template match="caution//*">
        <copy>
            <copy-of select="paragraph"/>
            <apply-templates/>
        </copy>
    </template>

<template match="paragraph/emphasis">*<apply-templates/>*</template>
<template match="paragraph/strong">**<apply-templates/>**</template>
<template match="paragraph/reference">[<value-of select="@name"/>](<value-of select="nn:urlencode(@refuri)"/>)</template>

    <template match="text()"/>
    <template match="paragraph//text()">
<choose>
<when test="position()=0"><copy-of select="."/></when>
<when test="position()=last()"><copy-of select="."/><text></text></when>
<otherwise><copy-of select="."/></otherwise>
       </choose>
    </template>

</stylesheet>
