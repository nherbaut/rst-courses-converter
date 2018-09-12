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
    <template match="paragraph//*">
        <copy>
            <copy-of select="@*"/>
            <apply-templates/>
        </copy>
    </template>

    <template match="paragraph//emphasis">*<apply-templates/>*</template>
    <template match="paragraph//strong">**<apply-templates/>**</template>
    <template match="paragraph//reference">[<value-of select="@name"/>](<value-of select="nn:urlencode(@refuri)"/>)</template>

    <template match="text()"/>
    <template match="paragraph//text()">
        <copy-of select="."/>
    </template>

</stylesheet>
